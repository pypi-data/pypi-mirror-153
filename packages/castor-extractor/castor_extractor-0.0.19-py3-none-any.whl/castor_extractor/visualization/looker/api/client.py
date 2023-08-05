import logging
from typing import Callable, Iterator, List, Optional, Sequence, Tuple

from ....utils import Pager, PagerLogger
from ..env import page_size
from ..fields import format_fields
from .sdk import (
    Credentials,
    Dashboard,
    DBConnection,
    Folder,
    Look,
    LookmlModel,
    LookmlModelExplore,
    Project,
    User,
    init40,
)

logger = logging.getLogger(__name__)

COMMON_DASH_LOOK_FIELDS = (
    "id",
    "title",
    "description",
    "folder_id",
    "created_at",
    "deleted_at",
    "last_accessed_at",
    "last_viewed_at",
    "view_count",
    "user_id",
)
FOLDER_FIELDS = (
    "id",
    "name",
    "parent_id",
    "creator_id",
    "is_personal",
    "is_personal_descendant",
)

DASHBOARD_FIELDS = (
    *COMMON_DASH_LOOK_FIELDS,
    {
        "dashboard_elements": (
            "id",
            "type",
            {
                "query": ("model", "view", "fields"),
                "look": ("id", {"query": ("model", "view", "fields")}),
                "result_maker": ("id", {"query": ("model", "view", "fields")}),
            },
        )
    },
)

LOOK_FIELDS = (
    *COMMON_DASH_LOOK_FIELDS,
    "updated_at",
    "last_updater_id",
    "query_id",
    "is_run_on_load",
    "model",  # { id, label }
)

USER_FIELDS = ("id", "avatar_url", "display_name", "email", "is_disabled")
LOOKML_FIELDS = (
    "name",
    "label",
    "has_content",
    "project_name",
    {"explores": ("name", "description", "label", "hidden", "group_label")},
)

CONNECTION_FIELDS = (
    "name",
    "dialect",
    "pdts_enabled",
    "host",
    "database",
    "schema",
    "tmp_db_name",
    "jdbc_additional_params",
    "dialect_name",
    "created_at",
    "user_id",
    "example",
    "user_attribute_fields",
    "sql_writing_with_info_schema",
)

PROJECT_FIELDS = (
    "id",
    "name",
    "uses_git",
    "git_remote_url",
    "git_username",
    "git_production_branch_name",
    "use_git_cookie_auth",
    "git_password_user_attribute",
    "git_service_name",
    "git_application_server_http_port",
    "git_application_server_http_scheme",
    "pull_request_mode",
    "validation_required",
    "git_release_mgmt_enabled",
    "allow_warnings",
    "is_example",
)

EXPLORE_FIELD_FIELDS = (
    "description",
    "field_group_label",
    "field_group_variant",
    "hidden",
    "is_filter",
    "label",
    "label_short",
    "measure",
    "name",
    "parameter",
    "primary_key",
    "project_name",
    "scope",
    "sortable",
    "sql",
    "tags",  # string[]
    "type",
    "view",
    "view_label",
    "times_used",
)

EXPLORE_JOIN_FIELDS = (
    "name",
    "dependent_fields",  # string[]
    "fields",  # string[]
    "foreign_key",
    "from_",
    "outer_only",
    "relationship",
    "required_joins",  # string[]
    "sql_foreign_key",
    "sql_on",
    "sql_table_name",
    "type",
    "view_label",
)

EXPLORE_FIELDS = (
    "id",
    "description",
    "name",
    "label",
    "title",
    "scopes",  # string[]
    "project_name",
    "model_name",
    "view_name",
    "hidden",
    "sql_table_name",
    "group_label",
    "tags",  # string[]
    {
        "fields": {
            "dimensions": EXPLORE_FIELD_FIELDS,
            "measures": EXPLORE_FIELD_FIELDS,
        },
        "joins": EXPLORE_JOIN_FIELDS,
    },
)

# Model from looker
LOOKML_PROJECT_NAME_BLOCKLIST = ("looker-data", "system__activity")


OnApiCall = Callable[[], None]


class ApiPagerLogger(PagerLogger):
    def __init__(self, on_api_call: Optional[OnApiCall]):
        self._on_api_call = on_api_call

    def on_page(self, page: int, count: int):
        logger.info(f"Fetched page {page} / {count} results")
        self._on_api_call and self._on_api_call()

    def on_success(self, page: int, total: int):
        logger.info(f"All page fetched: {page} pages / {total} results")


class ApiClient:
    """Looker client"""

    def __init__(
        self, credentials: Credentials, on_api_call: OnApiCall = lambda: None
    ):
        self._sdk = init40(credentials)
        self._on_api_call = on_api_call
        self._logger = ApiPagerLogger(on_api_call)
        self.per_page = page_size()

    def folders(self) -> List[Folder]:
        """Lists folders of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[Folder]:
            return self._sdk.search_folders(
                fields=format_fields(FOLDER_FIELDS),
                per_page=per_page,
                page=page,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def dashboards(self) -> List[Dashboard]:
        """Lists dashboards of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[Dashboard]:
            return self._sdk.search_dashboards(
                fields=format_fields(DASHBOARD_FIELDS),
                per_page=per_page,
                page=page,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def looks(self) -> List[Look]:
        """Lists looks of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[Look]:
            return self._sdk.search_looks(
                fields=format_fields(LOOK_FIELDS), per_page=per_page, page=page
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def users(self) -> List[User]:
        """Lists users of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[User]:
            # HACK:
            # We use verified_looker_employee=False (filter out Looker employees)
            # Else api returns an empty list when no parameters are specified
            return self._sdk.search_users(
                fields=format_fields(USER_FIELDS),
                per_page=per_page,
                page=page,
                verified_looker_employee=False,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def lookml_models(self) -> List[LookmlModel]:
        """Iterates LookML models of the given Looker account"""

        models = self._sdk.all_lookml_models(
            fields=format_fields(LOOKML_FIELDS)
        )

        logger.info("All LookML models fetched")
        self._on_api_call()

        return [
            model
            for model in models
            if model.project_name not in LOOKML_PROJECT_NAME_BLOCKLIST
        ]

    def explores(
        self, explore_names=Iterator[Tuple[str, str]]
    ) -> List[LookmlModelExplore]:
        """Iterates explores of the given Looker account for the provided model/explore names"""

        def _call(model_name: str, explore_name: str) -> LookmlModelExplore:
            explore = self._sdk.lookml_model_explore(model_name, explore_name)

            logger.info(f"Explore {model_name}/{explore_name} fetched")
            self._on_api_call()
            return explore

        return [
            _call(model_name, explore_name)
            for model_name, explore_name in explore_names
        ]

    def connections(self) -> List[DBConnection]:
        """Lists databases connections of the given Looker account"""

        connections = self._sdk.all_connections(
            fields=format_fields(CONNECTION_FIELDS)
        )

        logger.info("All looker connections fetched")
        self._on_api_call()

        return list(connections)

    def projects(self) -> List[Project]:
        """Lists projects of the given Looker account"""

        projects = self._sdk.all_projects(fields=format_fields(PROJECT_FIELDS))

        logger.info("All looker projects fetched")
        self._on_api_call()

        return list(projects)
