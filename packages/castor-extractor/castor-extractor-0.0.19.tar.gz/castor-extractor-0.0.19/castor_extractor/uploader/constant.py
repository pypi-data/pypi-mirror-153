from enum import Enum


class FileType(Enum):
    """type of file to load"""

    DBT = "DBT"
    VIZ = "VIZ"
    WAREHOUSE = "WAREHOUSE"


BUCKETS = {
    FileType.DBT: "extraction-dbt",
    FileType.VIZ: "extraction-storage",
    FileType.WAREHOUSE: "extraction-storage",
}

PATH_TEMPLATES = {
    FileType.DBT: "warehouse-{source_id}/{timestamp}-manifest.json",
    FileType.VIZ: "visualization-{source_id}/{filename}",
    FileType.WAREHOUSE: "warehouse-{source_id}/{filename}",
}


"""
The default request timeout in seconds for the upload
"""
DEFAULT_TIMEOUT = 60.0
ENVIRON_TIMEOUT = "CASTOR_TIMEOUT_OVERRIDE"

"""
The default retry for the upload
"""
DEFAULT_RETRY = 1
ENVIRON_RETRY = "CASTOR_RETRY_OVERRIDE"
