import os
from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Dict, Optional

from sgqlc.endpoint.requests import RequestsEndpoint


class AbstractGQLClient(AbstractContextManager):
    @abstractmethod
    def execute(self, query, variables=None, operation_name=None, extra_headers=None, timeout=None):
        pass

    @staticmethod
    def _configure_gql_client(uri: str, headers: Optional[Dict] = None) -> RequestsEndpoint:
        env_timeout = os.getenv('GQL_API_TIMEOUT', None)
        timeout = float(env_timeout) if env_timeout is not None else None
        return RequestsEndpoint(uri, headers, timeout=timeout)
