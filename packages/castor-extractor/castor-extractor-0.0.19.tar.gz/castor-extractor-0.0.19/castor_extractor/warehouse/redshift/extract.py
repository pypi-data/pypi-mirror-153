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
from .client import RedshiftClient
from .query import RedshiftQueryBuilder

logger = logging.getLogger(__name__)

REDSHIFT_ASSETS: SupportedAssets = OrderedDict(
    {
        WarehouseAssetGroup.CATALOG: CATALOG_ASSETS,
        WarehouseAssetGroup.QUERY: QUERIES_ASSETS,
        WarehouseAssetGroup.VIEW_DDL: VIEWS_ASSETS,
        WarehouseAssetGroup.ROLE: (
            WarehouseAsset.USER,
            WarehouseAsset.GROUP,
        ),
    }
)

REDSHIFT_USER = "CASTOR_REDSHIFT_USER"
REDSHIFT_PASSWORD = "CASTOR_REDSHIFT_PASSWORD"
REDSHIFT_HOST = "CASTOR_REDSHIFT_HOST"
REDSHIFT_PORT = "CASTOR_REDSHIFT_PORT"
REDSHIFT_DATABASE = "CASTOR_REDSHIFT_DATABASE"


def _credentials(params: dict) -> dict:
    """extract Redshift credentials"""

    return {
        "user": params.get("user") or from_env(REDSHIFT_USER),
        "password": params.get("password") or from_env(REDSHIFT_PASSWORD),
        "host": params.get("host") or from_env(REDSHIFT_HOST),
        "port": params.get("port") or from_env(REDSHIFT_PORT),
        "database": params.get("database") or from_env(REDSHIFT_DATABASE),
    }


def extract_all(**kwargs) -> None:
    """
    Extract all assets from Redshift and store the results in CSV files
    """
    output_directory, skip_existing = common_args(kwargs)

    client = RedshiftClient(credentials=_credentials(kwargs))

    query_builder = RedshiftQueryBuilder()

    storage = LocalStorage(directory=output_directory)

    extractor = ExtractionProcessor(
        client=client, query_builder=query_builder, storage=storage
    )

    for group in REDSHIFT_ASSETS.values():
        for asset in group:
            logger.info(f"Extracting `{asset.value.upper()}` ...")
            location = extractor.extract(asset, skip_existing)
            logger.info(f"Results stored to {location}\n")

    write_summary(
        output_directory,
        storage.stored_at_ts,
        client_name=client.name(),
    )
