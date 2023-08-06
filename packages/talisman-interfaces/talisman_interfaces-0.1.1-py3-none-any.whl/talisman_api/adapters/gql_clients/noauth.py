from typing import Optional

from sgqlc.endpoint.requests import RequestsEndpoint

from .abstract import AbstractGQLClient


class NoAuthGQLClient(AbstractGQLClient):
    def __init__(self, gql_uri: str):
        self._gql_uri = gql_uri
        self._gql_client: Optional[RequestsEndpoint] = None

    def __enter__(self):
        self._gql_client = self._configure_gql_client(self._gql_uri)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._gql_client = None
        self._gql_client = None

    def execute(self, query, variables=None, operation_name=None, extra_headers=None, timeout=None):
        return self._gql_client(query, variables, operation_name, extra_headers, timeout)
