from enum import Enum
from typing import Dict

from .....utils import from_env


class CredentialsDbKey(Enum):
    HOST = "host"
    PORT = "port"
    DATABASE = "database"
    SCHEMA = "schema"
    USERNAME = "username"
    PASSWORD = "password"


CREDENTIALS_ENV: Dict[CredentialsDbKey, str] = {
    CredentialsDbKey.HOST: "CASTOR_METABASE_DB_HOST",
    CredentialsDbKey.PORT: "CASTOR_METABASE_DB_PORT",
    CredentialsDbKey.DATABASE: "CASTOR_METABASE_DB_DATABASE",
    CredentialsDbKey.SCHEMA: "CASTOR_METABASE_DB_SCHEMA",
    CredentialsDbKey.USERNAME: "CASTOR_METABASE_DB_USERNAME",
    CredentialsDbKey.PASSWORD: "CASTOR_METABASE_DB_PASSWORD",
}


def get_value(key: CredentialsDbKey, kwargs: dict) -> str:
    """
    Returns the value of the given key:
    - from kwargs in priority
    - from ENV if not provided (raises an error if not found in ENV)
    """
    env_key = CREDENTIALS_ENV[key]
    return str(kwargs.get(key.value) or from_env(env_key))


class CredentialsDb:
    """ValueObject for the credentials"""

    def __init__(
        self,
        host: str,
        port: str,
        database: str,
        schema: str,
        username: str,
        password: str,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.schema = schema
        self.username = username
        self.password = password

    def to_dict(self, hide: bool = False) -> Dict[str, str]:
        safe = (
            CredentialsDbKey.HOST,
            CredentialsDbKey.PORT,
            CredentialsDbKey.DATABASE,
            CredentialsDbKey.SCHEMA,
            CredentialsDbKey.USERNAME,
        )
        unsafe = (CredentialsDbKey.PASSWORD,)

        def val(k: CredentialsDbKey, v: str) -> str:
            return "*" + v[-4:] if hide and k in unsafe else v

        return {a.value: val(a, getattr(self, a.value)) for a in safe + unsafe}
