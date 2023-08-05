import logging
from typing import List

import tableauserverclient as TSC  # type: ignore

from ....utils import EntitiesType
from ..constants import PAGE_SIZE, TABLEAU_SERVER_VERSION
from ..entities import TableauEntity
from ..usage import compute_usage_views
from .client_utils import extract_entity, get_paginated_objects
from .credentials import CredentialsApi, CredentialsKey, get_value
from .project import compute_project_path
from .safe_mode import safe_mode_fetch_usage

logger = logging.getLogger(__name__)


class ApiClient:
    """
    Connect to Tableau REST API and fetch main entities.
    Superuser credentials are required.
    https://tableau.github.io/server-client-python/docs/
    """

    def __init__(
        self,
        **kwargs,
    ):
        self._credentials = CredentialsApi(
            user=get_value(CredentialsKey.TABLEAU_USER, kwargs, True),
            password=get_value(CredentialsKey.TABLEAU_PASSWORD, kwargs, True),
            token_name=get_value(
                CredentialsKey.TABLEAU_TOKEN_NAME, kwargs, True
            ),
            token=get_value(CredentialsKey.TABLEAU_TOKEN, kwargs, True),
            server_url=get_value(CredentialsKey.TABLEAU_SERVER_URL, kwargs),
            site_id=get_value(CredentialsKey.TABLEAU_SITE_ID, kwargs),
        )
        self._server = TSC.Server(self._credentials.server_url)
        self._server.add_http_options({"verify": True})
        self._page_size = PAGE_SIZE
        self._server.version = TABLEAU_SERVER_VERSION
        self._safe_mode = bool(kwargs.get("safe_mode"))
        self.errors: List[str] = []

    @staticmethod
    def name() -> str:
        return "Tableau/API"

    def _user_password_login(self) -> None:
        """Login into Tableau using user and password"""
        self._server.auth.sign_in(
            TSC.TableauAuth(
                self._credentials.user,
                self._credentials.password,
                site_id=self._credentials.site_id,
            )
        )

    def _pat_login(self) -> None:
        """Login into Tableau using personal authentication token"""
        self._server.auth.sign_in(
            TSC.PersonalAccessTokenAuth(
                self._credentials.token_name,
                self._credentials.token,
                site_id=self._credentials.site_id,
            )
        )

    def login(self) -> None:
        """Login into Tableau"""

        if self._credentials.user and self._credentials.password:
            logger.info("Logging in using user and password authentication")
            return self._user_password_login()

        if self._credentials.token_name and self._credentials.token:
            logger.info("Logging in using token authentication")
            return self._pat_login()

        raise ValueError(
            """Wrong authentication: you should provide either user and password
             or personal access token"""
        )

    def base_url(self) -> str:
        return self._credentials.server_url

    def _fetch_users(self) -> EntitiesType:
        """Fetches list of User"""
        return [
            extract_entity(user, TableauEntity.USER)
            for user in TSC.Pager(self._server.users)
        ]

    def _fetch_workbooks(self) -> EntitiesType:
        """Fetches list of Workbooks"""

        return [
            extract_entity(workbook, TableauEntity.WORKBOOK)
            for workbook in TSC.Pager(self._server.workbooks)
        ]

    def _fetch_usages(self, safe_mode: bool) -> EntitiesType:
        """Fetches list of Usages"""
        if not safe_mode:
            usages = [
                extract_entity(usage, TableauEntity.USAGE)
                for usage in TSC.Pager(self._server.views, usage=True)
            ]

            return compute_usage_views(usages)

        return safe_mode_fetch_usage(self)

    def _fetch_projects(self) -> EntitiesType:
        """Fetches list of Projects"""
        return compute_project_path(
            [
                extract_entity(project, TableauEntity.PROJECT)
                for project in TSC.Pager(self._server.projects)
            ]
        )

    def _fetch_workbooks_to_datasource(self) -> EntitiesType:
        """Fetches workbooks to datasource"""

        return self._fetch_paginated_objects(
            TableauEntity.WORKBOOK_TO_DATASOURCE,
        )

    def _fetch_datasources(self) -> EntitiesType:
        """Fetches datasource"""

        return self._fetch_paginated_objects(
            TableauEntity.DATASOURCE,
        )

    def _fetch_custom_sql_queries(self) -> EntitiesType:
        """Fetches custom sql queries"""

        return self._fetch_paginated_objects(
            TableauEntity.CUSTOM_SQL_QUERY,
        )

    def _fetch_custom_sql_tables(self) -> EntitiesType:
        """Fetches custom sql tables"""

        return self._fetch_paginated_objects(
            TableauEntity.CUSTOM_SQL_TABLE,
        )

    def _fetch_paginated_objects(self, entity: TableauEntity) -> EntitiesType:
        """Fetches paginated objects"""

        return get_paginated_objects(self._server, entity, self._page_size)

    def fetch(self, entity: TableauEntity) -> EntitiesType:
        """Fetches the given entity"""
        logger.info(f"Fetching {entity.name}")

        if entity == TableauEntity.USER:
            entities = self._fetch_users()

        if entity == TableauEntity.USAGE:
            entities = self._fetch_usages(self._safe_mode)

        if entity == TableauEntity.PROJECT:
            entities = self._fetch_projects()

        if entity == TableauEntity.WORKBOOK:
            entities = self._fetch_workbooks()

        if entity == TableauEntity.WORKBOOK_TO_DATASOURCE:
            entities = self._fetch_workbooks_to_datasource()

        if entity == TableauEntity.DATASOURCE:
            entities = self._fetch_datasources()

        if entity == TableauEntity.CUSTOM_SQL_TABLE:
            entities = self._fetch_custom_sql_tables()

        if entity == TableauEntity.CUSTOM_SQL_QUERY:
            entities = self._fetch_custom_sql_queries()

        logger.info(f"Fetched {entity.name} ({len(entities)} results)")

        return entities
