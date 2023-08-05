import logging
from collections import OrderedDict

from ...utils import LocalStorage, from_env, write_summary
from ..abstract import (
    CATALOG_ASSETS,
    QUERIES_ASSETS,
    VIEWS_ASSETS,
    ExtractionProcessor,
    SupportedAssets,
    WarehouseAsset,
    WarehouseAssetGroup,
    common_args,
)
from .client import SnowflakeClient
from .query import SnowflakeQueryBuilder

logger = logging.getLogger(__name__)

SNOWFLAKE_ASSETS: SupportedAssets = OrderedDict(
    {
        WarehouseAssetGroup.CATALOG: CATALOG_ASSETS,
        WarehouseAssetGroup.QUERY: QUERIES_ASSETS,
        WarehouseAssetGroup.VIEW_DDL: VIEWS_ASSETS,
        WarehouseAssetGroup.ROLE: (
            WarehouseAsset.GRANT_TO_ROLE,
            WarehouseAsset.GRANT_TO_USER,
            WarehouseAsset.ROLE,
            WarehouseAsset.USER,
        ),
    }
)

SNOWFLAKE_ACCOUNT = "CASTOR_SNOWFLAKE_ACCOUNT"
SNOWFLAKE_USER = "CASTOR_SNOWFLAKE_USER"
SNOWFLAKE_PASSWORD = "CASTOR_SNOWFLAKE_PASSWORD"


def _credentials(params: dict) -> dict:
    """extract Snowflake credentials"""

    return {
        "account": params.get("account") or from_env(SNOWFLAKE_ACCOUNT),
        "user": params.get("user") or from_env(SNOWFLAKE_USER),
        "password": params.get("password") or from_env(SNOWFLAKE_PASSWORD),
    }


def extract_all(**kwargs) -> None:
    """
    Extract all assets from Snowflake and store the results in CSV files
    """
    output_directory, skip_existing = common_args(kwargs)

    client = SnowflakeClient(
        credentials=_credentials(kwargs),
        warehouse=kwargs.get("warehouse"),
        role=kwargs.get("role"),
    )

    query_builder = SnowflakeQueryBuilder(
        db_allowed=kwargs.get("db_allowed"),
        db_blocked=kwargs.get("db_blocked"),
        fetch_transient=kwargs.get("fetch_transient"),
    )

    storage = LocalStorage(directory=output_directory)

    extractor = ExtractionProcessor(
        client=client, query_builder=query_builder, storage=storage
    )

    for group in SNOWFLAKE_ASSETS.values():
        for asset in group:
            logger.info(f"Extracting `{asset.value.upper()}` ...")
            location = extractor.extract(asset, skip_existing)
            logger.info(f"Results stored to {location}\n")

    write_summary(
        output_directory,
        storage.stored_at_ts,
        client_name=client.name(),
    )
