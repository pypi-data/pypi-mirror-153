from enum import Enum
from typing import Dict

from requests.auth import HTTPBasicAuth

from ....utils import from_env


class CredentialsKey(Enum):
    HOST = "host"
    WORKSPACE = "workspace"
    TOKEN = "token"
    SECRET = "secret"


CREDENTIALS_ENV: Dict[CredentialsKey, str] = {
    CredentialsKey.HOST: "CASTOR_MODE_ANALYTICS_HOST",
    CredentialsKey.WORKSPACE: "CASTOR_MODE_ANALYTICS_WORKSPACE",
    CredentialsKey.TOKEN: "CASTOR_MODE_ANALYTICS_TOKEN",
    CredentialsKey.SECRET: "CASTOR_MODE_ANALYTICS_SECRET",
}


def get_value(key: CredentialsKey, kwargs: dict) -> str:
    """
    Returns the value of the given key:
    - from kwargs in priority
    - from ENV if not provided (raises an error if not found in ENV)
    """
    env_key = CREDENTIALS_ENV[key]
    return str(kwargs.get(key.value) or from_env(env_key))


class Credentials:
    """ValueObject for the credentials"""

    def __init__(self, host: str, workspace: str, token: str, secret: str):
        self.host = host
        self.workspace = workspace
        self.token = token
        self.secret = secret

    def to_dict(self, hide: bool = False) -> Dict[str, str]:
        safe = (
            CredentialsKey.HOST,
            CredentialsKey.WORKSPACE,
            CredentialsKey.TOKEN,
        )
        unsafe = (CredentialsKey.SECRET,)

        def val(k: CredentialsKey, v: str) -> str:
            return "*" + v[-4:] if hide and k in unsafe else v

        return {a.value: val(a, getattr(self, a.value)) for a in safe + unsafe}

    def authentication(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.token, self.secret)
