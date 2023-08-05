from enum import Enum
from typing import Dict

from .....utils import from_env


class CredentialsApiKey(Enum):
    BASE_URL = "base_url"
    USERNAME = "username"
    PASSWORD = "password"


CREDENTIALS_ENV: Dict[CredentialsApiKey, str] = {
    CredentialsApiKey.BASE_URL: "CASTOR_METABASE_API_BASE_URL",
    CredentialsApiKey.USERNAME: "CASTOR_METABASE_API_USERNAME",
    CredentialsApiKey.PASSWORD: "CASTOR_METABASE_API_PASSWORD",
}


def get_value(key: CredentialsApiKey, kwargs: dict) -> str:
    """
    Returns the value of the given key:
    - from kwargs in priority
    - from ENV if not provided (raises an error if not found in ENV)
    """
    env_key = CREDENTIALS_ENV[key]
    return str(kwargs.get(key.value) or from_env(env_key))


class CredentialsApi:
    """ValueObject for the credentials"""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

    def to_dict(self, hide: bool = False) -> Dict[str, str]:
        safe = (CredentialsApiKey.BASE_URL, CredentialsApiKey.USERNAME)
        unsafe = (CredentialsApiKey.PASSWORD,)

        def val(k: CredentialsApiKey, v: str) -> str:
            return "*" + v[-4:] if hide and k in unsafe else v

        return {a.value: val(a, getattr(self, a.value)) for a in safe + unsafe}
