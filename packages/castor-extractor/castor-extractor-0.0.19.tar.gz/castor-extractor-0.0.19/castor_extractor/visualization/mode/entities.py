from enum import Enum


class ModeAnalyticsEntity(Enum):
    """
    Entities that can be fetched from Mode Analytics
    """

    DATASOURCE = "data_sources"
    REPORT = "reports"
    COLLECTION = "spaces"  # legacy name, still valid in the API
    MEMBER = "user"
    QUERY = "queries"


ENTITIES_WITH_OWNER = (
    ModeAnalyticsEntity.COLLECTION,
    ModeAnalyticsEntity.REPORT,
)


EXPORTED_FIELDS = {
    ModeAnalyticsEntity.DATASOURCE: (
        "id",
        "token",
        "name",
        "host",
        "display_name",
        "description",
        "database",
        "provider",
        "vendor",
        "adapter",
        "created_at",
        "public",
        "queryable",
    ),
    ModeAnalyticsEntity.MEMBER: (
        "id",
        "token",
        "username",
        "name",
        "email",
        "created_at",
    ),
    ModeAnalyticsEntity.REPORT: (
        "id",
        "token",
        "name",
        "description",
        "type",
        "archived",
        "space_token",
        "public",
        "created_at",
        "updated_at",
        "published_at",
        "edited_at",
        "is_embedded",
        "query_count",
        "chart_count",
        "view_count",
        "creator",
    ),
    ModeAnalyticsEntity.QUERY: (
        "id",
        "token",
        "name",
        "data_source_id",
        "raw_query",
        "report_token",
    ),
    ModeAnalyticsEntity.COLLECTION: (
        "id",
        "token",
        "space_type",
        "name",
        "description",
        "state",
        "default_access_level",
        "creator",
    ),
}
