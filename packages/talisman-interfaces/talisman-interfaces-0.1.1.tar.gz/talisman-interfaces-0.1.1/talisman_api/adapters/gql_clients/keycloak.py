import logging
import os
import time
from typing import Optional

from keycloak import KeycloakOpenID
from sgqlc.endpoint.requests import RequestsEndpoint

from .abstract import AbstractGQLClient

logger = logging.getLogger(__name__)


class KeycloakAwareGQLClient(AbstractGQLClient):
    _TIME_OFFSET = 10  # in seconds

    def __init__(self, gql_uri: str):
        self._gql_uri = gql_uri

        self._auth_url = os.getenv("KEYCLOAK_AUTH_URL")
        self._realm = os.getenv("KEYCLOAK_REALM")
        self._client_id = os.getenv("KEYCLOAK_CLIENT_ID")
        self._client_secret = os.getenv("KEYCLOAK_CLIENT_KEY")
        self._user = os.getenv("KEYCLOAK_USER")
        self._pwd = os.getenv("KEYCLOAK_PWD")

        if any(env is None for env in [self._auth_url, self._realm, self._client_id, self._client_secret, self._user, self._pwd]):
            raise ValueError("Authorization environment values are not set")

        self._keycloak_openid: Optional[KeycloakOpenID] = None
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._access_expiration_timestamp: Optional[float] = None
        self._refresh_expiration_timestamp: Optional[float] = None

        self._gql_client: Optional[RequestsEndpoint] = None

    def _ensure_session_liveness(self):
        offsetted_time = time.time() + self._TIME_OFFSET
        if self._access_expiration_timestamp is not None and offsetted_time < self._access_expiration_timestamp:
            return

        time_before_req = time.time()
        if self._refresh_expiration_timestamp is not None and offsetted_time < self._refresh_expiration_timestamp:
            logger.info("refreshing access token with refresh token")
            token_info = self._keycloak_openid.refresh_token(self._refresh_token)
        else:
            logger.info("refreshing access token with credentials")
            token_info = self._keycloak_openid.token(self._user, self._pwd)

        self._access_token = token_info['access_token']
        self._access_expiration_timestamp = time_before_req + token_info['expires_in']
        self._refresh_token = token_info['refresh_token']
        self._refresh_expiration_timestamp = time_before_req + token_info['refresh_expires_in']

        headers = {"X-Auth-Token": self._access_token, "Authorization": f"Bearer {self._access_token}"}
        self._gql_client = self._configure_gql_client(self._gql_uri, headers)

    def __enter__(self):
        self._keycloak_openid = KeycloakOpenID(self._auth_url, self._realm, self._client_id, self._client_secret)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._gql_client = None
        self._access_token, self._refresh_token = None, None
        self._access_expiration_timestamp, self._refresh_expiration_timestamp = None, None
        self._keycloak_openid, self._gql_client = None, None

    def execute(self, query, variables=None, operation_name=None, extra_headers=None, timeout=None):
        self._ensure_session_liveness()
        return self._gql_client(query, variables, operation_name, extra_headers, timeout)
