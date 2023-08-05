from typing import List, Optional

from ..abstract import (
    QUERIES_DIR,
    AbstractQueryBuilder,
    ExtractionQuery,
    TimeFilter,
    WarehouseAsset,
)

# Those queries must be formatted with {region}
from .typing import IterTwoString

REGION_REQUIRED = (
    WarehouseAsset.COLUMN,
    WarehouseAsset.DATABASE,
    WarehouseAsset.QUERY,
    WarehouseAsset.SCHEMA,
    WarehouseAsset.TABLE,
    WarehouseAsset.USER,
)

# Those queries must be formatted with {dataset}
DATASET_REQUIRED = (WarehouseAsset.VIEW_DDL,)

# Those queries must be de-duplicated
# The usage of DISTINCT in the query is not enough
# because we stitch several queries results
BIGQUERY_DUPLICATES = (
    WarehouseAsset.DATABASE,
    WarehouseAsset.USER,
)

SHARDED_ASSETS = (WarehouseAsset.TABLE, WarehouseAsset.COLUMN)
SHARDED_FILE_PATH = "cte/sharded.sql"


def _database_formatted(datasets: IterTwoString) -> str:
    databases = {db for _, db in datasets}
    if not databases:
        # when no datasets are provided condition should pass
        return "(NULL)"
    formatted = ", ".join([f"'{db}'" for db in databases])
    return f"({formatted})"


class BigQueryQueryBuilder(AbstractQueryBuilder):
    """
    Builds queries to extract assets from BigQuery.
    Generate multiple queries to support multi-regions
    """

    def __init__(
        self,
        regions: IterTwoString,
        datasets: IterTwoString,
        time_filter: Optional[TimeFilter] = None,
        sync_tags: Optional[bool] = False,
    ):
        super().__init__(
            time_filter=time_filter, duplicated=BIGQUERY_DUPLICATES
        )
        self._regions = regions
        self._datasets = datasets
        self._sync_tags = sync_tags

    @staticmethod
    def _format(query: ExtractionQuery, values: dict) -> ExtractionQuery:
        return ExtractionQuery(
            statement=query.statement.format(**values),
            params=query.params,
        )

    def file_name(self, asset: WarehouseAsset) -> str:
        """
        Returns the SQL filename extracting the given asset.
        Overrides the default behaviour - handle table tags for BigQuery
        """
        if asset == WarehouseAsset.TABLE and self._sync_tags:
            # Reading `INFORMATION_SCHEMA.SCHEMATA_OPTIONS` requires specific permissions.
            # Synchronization of tags is only activated when credentials are sufficient.
            return f"{asset.value}_with_tags.sql"

        return f"{asset.value}.sql"

    def load_statement(self, asset: WarehouseAsset) -> str:
        """load sql statement from file"""
        statement = super().load_statement(asset)

        if asset not in SHARDED_ASSETS:
            return statement

        sharded_statement = self._load_from_file(SHARDED_FILE_PATH)
        return statement.format(sharded_statement=sharded_statement)

    def build(self, asset: WarehouseAsset) -> List[ExtractionQuery]:
        """
        It would be easier to stitch data directly in the query statement (UNION ALL).
        Unfortunately, querying INFORMATION_SCHEMA on multiple regions
          at the same time gives partial result (seems like a BigQuery bug)
        This weird behaviour forces us to
          - run one query per tuple(project, region)
          -  stitch data afterwards.
        """
        query = super().build_default(asset)

        if asset in REGION_REQUIRED:
            return [
                self._format(query, {"project": project, "region": region})
                for project, region in self._regions
            ]

        if asset in DATASET_REQUIRED:
            return [
                self._format(query, {"project": project, "dataset": dataset})
                for project, dataset in self._datasets
            ]

        return [query]
