import logging
from collections import OrderedDict

from ..abstract import (
    CATALOG_ASSETS,
    QUERIES_ASSETS,
    VIEWS_ASSETS,
    SupportedAssets,
    WarehouseAsset,
    WarehouseAssetGroup,
)

logger = logging.getLogger(__name__)

SYNAPSE_ASSETS: SupportedAssets = OrderedDict(
    {
        WarehouseAssetGroup.CATALOG: CATALOG_ASSETS,
        WarehouseAssetGroup.QUERY: QUERIES_ASSETS,
        WarehouseAssetGroup.VIEW_DDL: VIEWS_ASSETS,
        WarehouseAssetGroup.ROLE: (WarehouseAsset.USER,),
    }
)
