import json
import logging
from collections import OrderedDict
from typing import cast

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
from .client import BigQueryClient
from .query import BigQueryQueryBuilder

logger = logging.getLogger(__name__)

BIGQUERY_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"


BIGQUERY_ASSETS: SupportedAssets = OrderedDict(
    {
        WarehouseAssetGroup.CATALOG: CATALOG_ASSETS,
        WarehouseAssetGroup.QUERY: QUERIES_ASSETS,
        WarehouseAssetGroup.VIEW_DDL: VIEWS_ASSETS,
        WarehouseAssetGroup.ROLE: (WarehouseAsset.USER,),
    }
)


def _credentials(params: dict) -> dict:
    """extract GCP credentials"""
    path = params.get("credentials") or from_env(BIGQUERY_CREDENTIALS)
    logger.info(f"Credentials fetched from {path}")
    with open(path) as file:
        return cast(dict, json.load(file))


def extract_all(**kwargs) -> None:
    """
    Extract all assets from BigQuery and store the results in CSV files
    Time filter scope for `Queries` = the day before (0 > 23h)
    """
    output_directory, skip_existing = common_args(kwargs)

    client = BigQueryClient(
        credentials=_credentials(kwargs),
        db_allowed=kwargs.get("db_allowed"),
        db_blocked=kwargs.get("db_blocked"),
    )

    logger.info(f"Available projects: {client.get_projects()}\n")

    query_builder = BigQueryQueryBuilder(
        regions=client.get_regions(), datasets=client.get_datasets()
    )

    storage = LocalStorage(directory=output_directory)

    extractor = ExtractionProcessor(
        client=client, query_builder=query_builder, storage=storage
    )

    for group in BIGQUERY_ASSETS.values():
        for asset in group:
            logger.info(f"Extracting `{asset.value.upper()}` ...")
            location = extractor.extract(asset, skip_existing)
            logger.info(f"Results stored to {location}\n")

    write_summary(
        output_directory,
        storage.stored_at_ts,
        client_name=client.name(),
    )
