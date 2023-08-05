import logging
from typing import Iterable, Tuple

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    write_json,
    write_summary,
)
from .client import Client
from .entities import ModeAnalyticsEntity as Entity

logger = logging.getLogger(__name__)


def iterate_all_data(
    client: Client,
) -> Iterable[Tuple[Entity, list]]:
    """Iterate over the extracted Data From Mode Analytics"""

    datasources = client.fetch(Entity.DATASOURCE)
    yield Entity.DATASOURCE, deep_serialize(datasources)

    collections = client.fetch(Entity.COLLECTION)
    yield Entity.COLLECTION, deep_serialize(collections)

    reports = client.fetch(Entity.REPORT, additional_data=collections)
    yield Entity.REPORT, deep_serialize(reports)

    queries = client.fetch(Entity.QUERY, additional_data=reports)
    yield Entity.QUERY, deep_serialize(queries)

    members = client.fetch(Entity.MEMBER)
    yield Entity.MEMBER, deep_serialize(members)


def extract_all(client: Client, **kwargs: str) -> None:
    """Extract Data From Mode Analytics and store it locally in files under the output_directory"""
    output_directory = kwargs.get("output_directory") or from_env(OUTPUT_DIR)
    ts = current_timestamp()

    for key, data in iterate_all_data(client):
        filename = get_output_filename(key.name.lower(), output_directory, ts)
        write_json(filename, data)

    write_summary(
        output_directory,
        ts,
        base_url=client.base_url(),
        client_name=client.name(),
    )
