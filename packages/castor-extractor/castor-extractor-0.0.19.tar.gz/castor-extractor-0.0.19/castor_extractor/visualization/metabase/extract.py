import logging
from typing import Iterable, Tuple, Union

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    write_json,
    write_summary,
)
from .client import ApiClient, DbClient
from .entities import MetabaseEntity

logger = logging.getLogger(__name__)

ClientMetabase = Union[DbClient, ApiClient]


def iterate_all_data(
    client: ClientMetabase,
) -> Iterable[Tuple[MetabaseEntity, list]]:
    """Iterate over the extracted Data From metabase"""

    yield MetabaseEntity.USER, deep_serialize(client.fetch(MetabaseEntity.USER))
    yield MetabaseEntity.COLLECTION, deep_serialize(
        client.fetch(MetabaseEntity.COLLECTION)
    )
    yield MetabaseEntity.DATABASE, deep_serialize(
        client.fetch(MetabaseEntity.DATABASE)
    )
    yield MetabaseEntity.TABLE, deep_serialize(
        client.fetch(MetabaseEntity.TABLE)
    )
    yield MetabaseEntity.CARD, deep_serialize(client.fetch(MetabaseEntity.CARD))
    yield MetabaseEntity.DASHBOARD, deep_serialize(
        client.fetch(MetabaseEntity.DASHBOARD)
    )
    yield MetabaseEntity.DASHBOARD_CARDS, deep_serialize(
        client.fetch(MetabaseEntity.DASHBOARD_CARDS)
    )


def extract_all(client: ClientMetabase, **kwargs: str) -> None:
    """
    Extract Data From metabase
    Store the output files locally under the given output_directory
    """
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
