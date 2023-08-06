import logging
import os
from contextlib import AbstractContextManager
from typing import Callable, Dict, Iterable, Iterator, Optional, Tuple, Union

from requests import Timeout
from sgqlc.operation import GraphQLErrors, Operation
from sgqlc.types import Variable

from .gql_clients import AbstractGQLClient, KeycloakAwareGQLClient, NoAuthGQLClient
from .schemas.api_schema import ConceptPropertyValueType, ConceptType, Query

logger = logging.getLogger(__name__)


class TalismanAPIAdapter(AbstractContextManager):
    def __init__(self, gql_uris: Union[str, Tuple[str, ...]]):
        self._gql_uris = (gql_uris,) if isinstance(gql_uris, str) else gql_uris
        self._gql_clients: Optional[Tuple[AbstractGQLClient, ...]] = None

    def __enter__(self):
        self._check_api()
        if os.getenv("KEYCLOAK_AUTH_URL") is None:
            self._gql_clients = tuple(NoAuthGQLClient(uri) for uri in self._gql_uris)
        else:
            self._gql_clients = tuple(KeycloakAwareGQLClient(uri) for uri in self._gql_uris)

        logger.info(f"{type(self._gql_clients[0])} will be used")

        for gql_client in self._gql_clients:
            gql_client.__enter__()
        return self

    def __exit__(self, *exc):
        for gql_client in reversed(self._gql_clients):
            gql_client.__exit__(*exc)
        self._gql_clients = None

    def _check_api(self):
        logger.info(f"used correct version of API")
        return True

    def get_base_types(self, dictionary: bool = False, regexp: bool = False, pretrained_nercmodels: bool = False
                       ) -> Tuple[Tuple[ConceptType, ...], Tuple[ConceptPropertyValueType, ...]]:
        op = Operation(Query)

        concept_types: ConceptType = op.list_concept_type
        property_value_types: ConceptPropertyValueType = op.list_concept_property_value_type

        concept_types.id()
        property_value_types.id()

        if dictionary:
            concept_types.dictionary()
            property_value_types.dictionary()

        if regexp:
            concept_types.regexp()
            property_value_types.regexp()

        if pretrained_nercmodels:
            concept_types.pretrained_nercmodels()
            property_value_types.pretrained_nercmodels()

        ret = self.gql_call(op)
        return tuple(ret.list_concept_type), tuple(ret.list_concept_property_value_type)

    def execute_easy_query(self, name: str, params: Iterable[str], variables: Optional[Dict] = None):
        op = Operation(Query)
        if variables:
            op[name](**variables).__fields__(*params)
        else:
            op[name].__fields__(*params)
        return self.gql_call(op)[name]

    def pagination_query(
            self,
            pagination_query: str, query_params: dict,
            list_query: str, list_query_builder: Callable[[Operation], None]
    ) -> Iterator:
        offset = 0
        # prepare operation
        op = Operation(Query, variables={"offset": int})
        pagination = op[pagination_query](**query_params, offset=Variable("offset"))
        pagination.total()
        list_query_builder(pagination[list_query]())

        # get first batch
        ret = self.gql_call(op, {"offset": offset})[pagination_query]
        total = ret.total
        yield from ret[list_query]

        # request until all items paginated
        offset += len(ret[list_query])
        while offset < total:  # while not
            ret = self.gql_call(op, {"offset": offset})[pagination_query]
            if not ret[list_query]:
                raise Exception("Empty query result")
            yield from ret[list_query]
            offset += len(ret[list_query])

    def _gql_call(self, gql_client: AbstractGQLClient, sgqlc_operation: Operation, variables: Optional[dict] = None,
                  raise_on_timeout: bool = True, raise_on_query: bool = False):
        try:
            return sgqlc_operation + gql_client.execute(sgqlc_operation, variables=variables)
        except Timeout as e:
            logger.error('Timeout while query processing', exc_info=e, extra={'query': sgqlc_operation})
            if raise_on_timeout:
                raise e
        except GraphQLErrors as e:
            logger.error(f"GraphQL exception '{e.errors[0]['message']}' during query processing.", exc_info=e,
                         extra={'query': sgqlc_operation})

            if raise_on_query or 'Cannot query field' not in e.errors[0]['message']:
                raise e
        except Exception as e:
            logger.error('Some exception was occured during query processing.', exc_info=e,
                         extra={'query': sgqlc_operation})
            raise e

    def gql_call(self, sgqlc_operation: Operation, variables: Optional[dict] = None, raise_on_timeout: bool = True):
        for gql_client in self._gql_clients[:-1]:
            res = self._gql_call(gql_client, sgqlc_operation, variables, raise_on_timeout)

            if res is not None:
                return res

        return self._gql_call(self._gql_clients[-1], sgqlc_operation, variables, raise_on_timeout, raise_on_query=True)
