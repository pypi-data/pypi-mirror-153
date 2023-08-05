from ...utils import uri_encode
from ..abstract import SqlalchemyClient

REDSHIFT_URI = "redshift+psycopg2://{user}:{password}@{host}:{port}/{database}"

DEFAULT_PORT = 5439


class RedshiftClient(SqlalchemyClient):
    """redshift client"""

    @staticmethod
    def name() -> str:
        return "Redshift"

    def _engine_options(self, credentials: dict) -> dict:
        return {"connect_args": {"sslmode": "verify-ca"}}

    def _build_uri(self, credentials: dict) -> str:
        return REDSHIFT_URI.format(
            user=credentials["user"],
            password=uri_encode(credentials["password"]),
            host=credentials["host"],
            port=credentials.get("port") or DEFAULT_PORT,
            database=credentials["database"],
        )
