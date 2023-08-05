from enum import Enum
from typing import Dict


class TableauEntity(Enum):
    """
    Entities which can be fetched from Tableau
    """

    WORKBOOK = "workbooks"
    USER = "users"
    PROJECT = "projects"
    USAGE = "views"
    WORKBOOK_TO_DATASOURCE = "workbooks_to_datasource"
    DATASOURCE = "datasources"
    CUSTOM_SQL_TABLE = "custom_sql_tables"
    CUSTOM_SQL_QUERY = "custom_sql_queries"


EXPORTED_FIELDS = {
    TableauEntity.WORKBOOK: (
        "id",
        "name",
        "description",
        "tags",
        "project_id",
        "created_at",
        "updated_at",
        "owner_id",
        "webpage_url",
    ),
    TableauEntity.PROJECT: (
        "id",
        "name",
        "description",
        "parent_id",
    ),
    TableauEntity.USER: (
        "id",
        "name",
        "email",
        "fullname",
        "site_role",
    ),
    TableauEntity.USAGE: (
        "workbook_id",
        "total_views",
    ),
}


class TableauGraphqlEntity(Enum):
    """
    Entities which can be fetched from Tableau
    """

    WORKBOOK_TO_DATASOURCE = "workbooks"
    DATASOURCE = "datasources"
    CUSTOM_SQL = "customSQLTables"

    """
    Fields which will be use for Tableau GraphQL API
    """

    FIELDS_WORKBOOK_TO_DATASOURCE = """
        luid
        id
        embeddedDatasources {
            id
            name
        }
    """

    FIELDS_DATASOURCE = """
        id
        name
        hasExtracts
        upstreamTables {
            id
            schema
            name
            fullName
            database {
                id
                name
                connectionType
            }
        }
    """

    FIELDS_CUSTOM_SQL_TABLE = """
        id
        name
        columns {
            referencedByFields {
                datasource {
                    ... on PublishedDatasource {
                        id
                    }

                    ... on EmbeddedDatasource {
                        id
                    }
                }
            }
        }
        """

    FIELDS_CUSTOM_SQL_QUERY = """
        id
        name
        query
        database {
            name
            connectionType
        }
        tables {
            name
        }
    """


QUERY_FIELDS: Dict[TableauEntity, Dict[str, TableauGraphqlEntity]] = {
    TableauEntity.WORKBOOK_TO_DATASOURCE: {
        "object_type": TableauGraphqlEntity.WORKBOOK_TO_DATASOURCE,
        "fields": TableauGraphqlEntity.FIELDS_WORKBOOK_TO_DATASOURCE,
    },
    TableauEntity.DATASOURCE: {
        "object_type": TableauGraphqlEntity.DATASOURCE,
        "fields": TableauGraphqlEntity.FIELDS_DATASOURCE,
    },
    TableauEntity.CUSTOM_SQL_TABLE: {
        "object_type": TableauGraphqlEntity.CUSTOM_SQL,
        "fields": TableauGraphqlEntity.FIELDS_CUSTOM_SQL_TABLE,
    },
    TableauEntity.CUSTOM_SQL_QUERY: {
        "object_type": TableauGraphqlEntity.CUSTOM_SQL,
        "fields": TableauGraphqlEntity.FIELDS_CUSTOM_SQL_QUERY,
    },
}
