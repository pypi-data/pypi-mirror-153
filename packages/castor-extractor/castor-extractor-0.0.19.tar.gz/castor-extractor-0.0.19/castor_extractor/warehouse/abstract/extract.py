import logging
from itertools import chain
from typing import Iterator, List, Tuple

from ...utils import OUTPUT_DIR, AbstractStorage, from_env
from .asset import WarehouseAsset
from .client import AbstractWarehouseClient
from .query import AbstractQueryBuilder

logger = logging.getLogger(__name__)


def common_args(kwargs: dict) -> Tuple[str, bool]:
    """Args used by all technologies"""
    output_directory = kwargs.get("output_directory") or from_env(OUTPUT_DIR)
    skip_existing = kwargs.get("skip_existing") or False
    return output_directory, skip_existing


class ExtractionProcessor:
    """extraction management"""

    def __init__(
        self,
        client: AbstractWarehouseClient,
        query_builder: AbstractQueryBuilder,
        storage: AbstractStorage,
    ):
        self._client = client
        self._query_builder = query_builder
        self._storage = storage

    @staticmethod
    def _unique(data: Iterator[dict]) -> List[dict]:
        """
        Remove duplicate in the given data.
        Remark: this method implies loading all data in memory: it breaks the streaming pipeline !
        """
        # dict > set > dict
        return [dict(t) for t in {tuple(d.items()) for d in data}]

    def _results(self, asset: WarehouseAsset) -> Iterator[dict]:

        data: Iterator[dict] = iter([])

        for query in self._query_builder.build(asset):
            # concatenate results of all queries
            data = chain(data, self._client.execute(query))

        if self._query_builder.needs_deduplication(asset):
            # cast the list to iterator, but the streaming pipeline is broken in that case
            return (row for row in self._unique(data))

        return data

    def extract(
        self, asset: WarehouseAsset, skip_existing: bool = False
    ) -> str:
        """
        Process extraction for the given asset and returns the location of extracted data
        """
        asset_name = asset.value
        if skip_existing and self._storage.exists(asset_name):
            logger.info("Skipped, file already exists")
            return self._storage.path(asset_name)

        try:
            data = self._results(asset)
            return self._storage.put(asset_name, data)
        finally:
            self._client.close()
