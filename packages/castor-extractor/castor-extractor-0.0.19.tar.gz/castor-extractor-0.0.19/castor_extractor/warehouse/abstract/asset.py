from enum import Enum
from typing import Dict, Tuple


class WarehouseAsset(Enum):
    """Assets that can be extracted from warehouses"""

    COLUMN = "column"
    DATABASE = "database"
    GRANT_TO_ROLE = "grant_to_role"
    GRANT_TO_USER = "grant_to_user"
    GROUP = "group"
    QUERY = "query"
    ROLE = "role"
    SCHEMA = "schema"
    TABLE = "table"
    USER = "user"
    VIEW_DDL = "view_ddl"


class WarehouseAssetGroup(Enum):
    """Groups of assets that can be extracted together"""

    CATALOG = "catalog"
    ROLE = "role"
    QUERY = "query"
    VIEW_DDL = "view_ddl"


# tuple of supported assets for each group (depends on the technology)
SupportedAssets = Dict[WarehouseAssetGroup, Tuple[WarehouseAsset, ...]]


# shared by all technologies
CATALOG_ASSETS = (
    WarehouseAsset.DATABASE,
    WarehouseAsset.SCHEMA,
    WarehouseAsset.TABLE,
    WarehouseAsset.COLUMN,
)

# shared by technologies supporting queries
QUERIES_ASSETS = (WarehouseAsset.QUERY,)
VIEWS_ASSETS = (WarehouseAsset.VIEW_DDL,)
