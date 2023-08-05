from enum import Enum
from typing import Dict, Optional

from ....utils import from_env

AUTH_ERROR_MSG = "Need either user and password or token_name and token"


class CredentialsKey(Enum):
    """Value enum object for the credentials"""

    TABLEAU_USER = "user"
    TABLEAU_PASSWORD = "password"
    TABLEAU_TOKEN_NAME = "token_name"
    TABLEAU_TOKEN = "token"
    TABLEAU_SITE_ID = "site_id"
    TABLEAU_SERVER_URL = "server_url"


CREDENTIALS_ENV: Dict[CredentialsKey, str] = {
    CredentialsKey.TABLEAU_USER: "CASTOR_TABLEAU_USER",
    CredentialsKey.TABLEAU_PASSWORD: "CASTOR_TABLEAU_PASSWORD",
    CredentialsKey.TABLEAU_TOKEN_NAME: "CASTOR_TABLEAU_TOKEN_NAME",
    CredentialsKey.TABLEAU_TOKEN: "CASTOR_TABLEAU_TOKEN",
    CredentialsKey.TABLEAU_SITE_ID: "CASTOR_TABLEAU_SITE_ID",
    CredentialsKey.TABLEAU_SERVER_URL: "CASTOR_TABLEAU_SERVER_URL",
}


def get_value(
    key: CredentialsKey, kwargs: dict, optional: bool = False
) -> Optional[str]:
    """
    Returns the value of the given key:
    - from kwargs in priority
    - from ENV if not provided (raises an error if not found in ENV)
    """
    env_key = CREDENTIALS_ENV[key]

    return kwargs.get(key.value) or from_env(env_key, optional)


class CredentialsApi:
    """ValueObject for the credentials"""

    def __init__(
        self,
        *,
        server_url: str,
        site_id: str,
        user: Optional[str],
        password: Optional[str],
        token_name: Optional[str],
        token: Optional[str],
    ):
        credentials = self._get_credentials(user, password, token_name, token)

        self.user = credentials.get(CredentialsKey.TABLEAU_USER)
        self.site_id = site_id
        self.server_url = server_url
        self.password = credentials.get(CredentialsKey.TABLEAU_PASSWORD)
        self.token_name = credentials.get(CredentialsKey.TABLEAU_TOKEN_NAME)
        self.token = credentials.get(CredentialsKey.TABLEAU_TOKEN)

    @staticmethod
    def _get_credentials(
        user: Optional[str],
        password: Optional[str],
        token_name: Optional[str],
        token: Optional[str],
    ) -> dict:
        """Helpers to retrieve credentials,
        if both are given choose user and password authentication method"""
        assert (user and password) or (token_name and token), AUTH_ERROR_MSG

        if user and password:
            return {
                CredentialsKey.TABLEAU_USER: user,
                CredentialsKey.TABLEAU_PASSWORD: password,
            }

        return {
            CredentialsKey.TABLEAU_TOKEN_NAME: token_name,
            CredentialsKey.TABLEAU_TOKEN: token,
        }

    def to_dict(self, hide: bool = False) -> Dict[str, str]:
        safe = (
            CredentialsKey.TABLEAU_USER,
            CredentialsKey.TABLEAU_SITE_ID,
            CredentialsKey.TABLEAU_SERVER_URL,
            CredentialsKey.TABLEAU_TOKEN_NAME,
        )
        unsafe = (CredentialsKey.TABLEAU_PASSWORD, CredentialsKey.TABLEAU_TOKEN)

        def val(k: CredentialsKey, v: str) -> str:
            return "*" + v[-4:] if hide and k in unsafe else v

        return {a.value: val(a, getattr(self, a.value)) for a in safe + unsafe}
