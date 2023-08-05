import logging
from typing import Iterable, Tuple

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    write_errors_logs,
    write_json,
    write_summary,
)
from .client import ApiClient as Client
from .entities import TableauEntity

logger = logging.getLogger(__name__)


def iterate_all_data(
    client: Client,
) -> Iterable[Tuple[TableauEntity, list]]:
    """Iterate over the extracted Data from Tableau"""

    logger.info("Extracting USER from Tableau API")
    yield TableauEntity.USER, deep_serialize(client.fetch(TableauEntity.USER))

    logger.info("Extracting WORKBOOK from Tableau API")
    yield TableauEntity.WORKBOOK, deep_serialize(
        client.fetch(TableauEntity.WORKBOOK)
    )

    logger.info("Extracting PROJECT from Tableau API")
    yield TableauEntity.PROJECT, deep_serialize(
        client.fetch(TableauEntity.PROJECT)
    )

    logger.info("Extracting USAGE from Tableau API")
    yield TableauEntity.USAGE, deep_serialize(client.fetch(TableauEntity.USAGE))

    logger.info("Extracting WORKBOOK_TO_DATASOURCE from Tableau API")
    yield TableauEntity.WORKBOOK_TO_DATASOURCE, deep_serialize(
        client.fetch(TableauEntity.WORKBOOK_TO_DATASOURCE)
    )

    logger.info("Extracting DATASOURCE from Tableau API")
    yield TableauEntity.DATASOURCE, deep_serialize(
        client.fetch(TableauEntity.DATASOURCE)
    )

    logger.info("Extracting CUSTOM_SQL_TABLE from Tableau API")
    yield TableauEntity.CUSTOM_SQL_TABLE, deep_serialize(
        client.fetch(TableauEntity.CUSTOM_SQL_TABLE)
    )

    logger.info("Extracting CUSTOM_SQL_QUERY from Tableau API")
    yield TableauEntity.CUSTOM_SQL_QUERY, deep_serialize(
        client.fetch(TableauEntity.CUSTOM_SQL_QUERY)
    )


def extract_all(client: Client, **kwargs: str) -> None:
    """
    Extract Data from tableau
    Store data locally in files under the output_directory
    If errors from Tableau's API are catch store them locally in file under the output_directory
    """
    output_directory = kwargs.get("output_directory") or from_env(OUTPUT_DIR)

    timestamp = current_timestamp()

    for key, data in iterate_all_data(client):
        filename = get_output_filename(key.value, output_directory, timestamp)
        write_json(filename, data)

    write_summary(
        output_directory,
        timestamp,
        base_url=client.base_url(),
        client_name=client.name(),
    )

    if client.errors:
        write_errors_logs(output_directory, timestamp, client.errors)
