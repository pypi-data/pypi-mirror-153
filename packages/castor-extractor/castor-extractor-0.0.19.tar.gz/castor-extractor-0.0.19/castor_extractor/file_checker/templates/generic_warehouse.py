from typing import Set

from ..column import ColumnChecker
from ..constants import COLUMN_TYPES, TABLE_TYPES
from ..enums import DataType
from ..file import FileTemplate


class GenericWarehouseFileTemplate:
    """
    Provides templates to validate generic warehouse files:
    - catalog: databases, schemas, tables, columns
    - users
    - queries
    - views DDL
    """

    @staticmethod
    def database() -> FileTemplate:
        return {
            "id": ColumnChecker(is_unique=True),
            "database_name": ColumnChecker(),
        }

    @staticmethod
    def schema(database_ids: Set[str]) -> FileTemplate:
        return {
            "id": ColumnChecker(is_unique=True),
            "database_id": ColumnChecker(foreign=database_ids),
            "schema_name": ColumnChecker(),
            "description": ColumnChecker(is_mandatory=False),
            "tags": ColumnChecker(is_mandatory=False),
        }

    @staticmethod
    def table(schema_ids: Set[str]) -> FileTemplate:
        return {
            "id": ColumnChecker(is_unique=True),
            "schema_id": ColumnChecker(foreign=schema_ids),
            "table_name": ColumnChecker(),
            "description": ColumnChecker(is_mandatory=False),
            "tags": ColumnChecker(is_mandatory=False),
            "type": ColumnChecker(enum_values=TABLE_TYPES),
        }

    @staticmethod
    def column(table_ids: Set[str]) -> FileTemplate:
        return {
            "id": ColumnChecker(is_unique=True),
            "table_id": ColumnChecker(foreign=table_ids),
            "column_name": ColumnChecker(),
            "description": ColumnChecker(is_mandatory=False),
            "data_type": ColumnChecker(enum_values=COLUMN_TYPES),
            "ordinal_position": ColumnChecker(
                is_mandatory=False, data_type=DataType.INTEGER
            ),
        }

    @staticmethod
    def query(database_ids: Set[str], user_ids: Set[str]) -> FileTemplate:
        return {
            "database_id": ColumnChecker(foreign=database_ids),
            "query_text": ColumnChecker(),
            "user_id": ColumnChecker(foreign=user_ids),
            "start_time": ColumnChecker(data_type=DataType.DATETIME),
            "end_time": ColumnChecker(
                data_type=DataType.DATETIME, is_mandatory=False
            ),
        }

    @staticmethod
    def view_ddl(
        database_ids: Set[str],
    ) -> FileTemplate:
        return {
            "database_id": ColumnChecker(foreign=database_ids),
            "view_name": ColumnChecker(is_mandatory=True),
            "definition": ColumnChecker(is_mandatory=True),
        }

    @staticmethod
    def user() -> FileTemplate:
        return {
            "id": ColumnChecker(is_unique=True),
            "email": ColumnChecker(is_mandatory=False),
            "first_name": ColumnChecker(is_mandatory=False),
            "last_name": ColumnChecker(is_mandatory=False),
        }
