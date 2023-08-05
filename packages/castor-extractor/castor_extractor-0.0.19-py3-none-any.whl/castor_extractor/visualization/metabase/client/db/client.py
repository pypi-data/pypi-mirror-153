import json
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from .....utils import EntitiesType, from_env
from ...entities import EXPORTED_FIELDS, MetabaseEntity
from ...errors import EncryptionSecretKeyRequired, MetabaseLoginError
from ..decryption import decrypt
from ..shared import DETAILS_KEY, get_dbname_from_details
from .credentials import CredentialsDb, CredentialsDbKey, get_value

logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PG_URL = "postgresql://{username}:{password}@{host}:{port}/{database}"
SQL_FILE_PATH = "queries/{name}.sql"

ENCRYPTION_SECRET_KEY = "CASTOR_METABASE_ENCRYPTION_SECRET_KEY"


class DbClient:
    """
    Connect to Metabase Database and fetch main entities.
    """

    def __init__(
        self,
        **kwargs,
    ):
        self._credentials = CredentialsDb(
            host=get_value(CredentialsDbKey.HOST, kwargs),
            port=get_value(CredentialsDbKey.PORT, kwargs),
            database=get_value(CredentialsDbKey.DATABASE, kwargs),
            schema=get_value(CredentialsDbKey.SCHEMA, kwargs),
            username=get_value(CredentialsDbKey.USERNAME, kwargs),
            password=get_value(CredentialsDbKey.PASSWORD, kwargs),
        )
        self.encryption_secret_key = kwargs.get(
            "encryption_secret_key"
        ) or from_env(ENCRYPTION_SECRET_KEY, allow_missing=True)
        self._engine = self._login()

    def _login(self) -> Engine:
        url = PG_URL.format(**self._credentials.to_dict(hide=False))
        try:
            engine = create_engine(url)
            engine.connect()
            return engine
        except OperationalError as err:
            raise MetabaseLoginError(
                credentials_info=self._credentials.to_dict(hide=True),
                error_details=err.args,
            )

    def _load_query(self, name: str) -> str:
        """load SQL text from file"""
        filename = SQL_FILE_PATH.format(name=name)
        path = os.path.join(CURRENT_DIR, filename)
        with open(path, "r") as f:
            content = f.read()
            return content.format(schema=self._credentials.schema)

    def _database_specifics(self, databases: EntitiesType) -> EntitiesType:
        for db in databases:
            assert DETAILS_KEY in db  # this field is expected in database table

            try:
                details = json.loads(db[DETAILS_KEY])
            except json.decoder.JSONDecodeError as err:
                if not self.encryption_secret_key:
                    raise EncryptionSecretKeyRequired(
                        credentials_info=self._credentials.to_dict(hide=True),
                        error_details=err.args,
                    )
                decrypted = decrypt(db[DETAILS_KEY], self.encryption_secret_key)
                details = json.loads(decrypted)

            db["dbname"] = get_dbname_from_details(details)

        return databases

    @staticmethod
    def name() -> str:
        """return the name of the client"""
        return "Metabase/DB"

    def base_url(self) -> str:
        """Fetches the `base_url` of the Metabase instance"""
        query = self._load_query(name="base_url")
        result = self._engine.execute(query)
        return result.fetchone()["value"]

    def fetch(self, entity: MetabaseEntity) -> EntitiesType:
        """fetches the given entity"""
        query = self._load_query(entity.value.lower())
        result = self._engine.execute(query)

        # convert row proxies into dictionaries
        entities = [
            {column: value for column, value in rowproxy.items()}
            for rowproxy in result
        ]

        if entity == MetabaseEntity.DATABASE:
            entities = self._database_specifics(entities)

        logger.info(f"Fetching {entity.name} ({len(entities)} results)")

        # keep interesting fields
        return [
            {key: e.get(key) for key in EXPORTED_FIELDS[entity]}
            for e in entities
        ]
