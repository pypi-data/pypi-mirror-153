from typing import List, Optional, Set, Tuple

from google.cloud.bigquery import Client as GoogleCloudClient  # type: ignore
from google.oauth2.service_account import Credentials  # type: ignore

from ..abstract import SqlalchemyClient

BIGQUERY_URI = "bigquery://"

CREDENTIALS_INFO_KEY = "credentials_info"
PROJECT_ID_KEY = "project_id"


class BigQueryClient(SqlalchemyClient):
    """Connect to BigQuery and run SQL queries"""

    def __init__(
        self,
        credentials: dict,
        db_allowed: Optional[Set[str]] = None,
        db_blocked: Optional[Set[str]] = None,
    ):
        super().__init__(credentials)
        self._db_allowed = db_allowed
        self._db_blocked = db_blocked

    @staticmethod
    def name() -> str:
        return "BigQuery"

    def _keep_project(self, project: str) -> bool:
        if self._db_allowed and project not in self._db_allowed:
            return False
        if self._db_blocked and project in self._db_blocked:
            return False
        return True

    def _engine_options(self, credentials: dict) -> dict:
        return {
            CREDENTIALS_INFO_KEY: credentials,
        }

    def _build_uri(self, credentials: dict) -> str:
        return BIGQUERY_URI

    def _google_cloud_client(self) -> GoogleCloudClient:
        assert (
            CREDENTIALS_INFO_KEY in self._options
        ), "Missing BigQuery credentials in engine's options"
        credentials = self._options[CREDENTIALS_INFO_KEY]
        return GoogleCloudClient(
            project=credentials.get(PROJECT_ID_KEY),
            credentials=Credentials.from_service_account_info(credentials),
        )

    def _list_datasets(self) -> List:
        client = self._google_cloud_client()
        return [
            dataset
            for project in client.list_projects()
            for dataset in client.list_datasets(project.project_id)
            if self._keep_project(project.project_id)
        ]

    def get_projects(self) -> List[str]:
        """
        Returns distinct project_id available for the given GCP client
        """
        client = self._google_cloud_client()
        return [
            p.project_id
            for p in client.list_projects()
            if self._keep_project(p.project_id)
        ]

    def get_regions(self) -> Set[Tuple[str, str]]:
        """
        Returns distinct (project_id, region) available for the given GCP client
        """
        return set(
            (ds.project, ds._properties["location"])
            for ds in self._list_datasets()
        )

    def get_datasets(self) -> Set[Tuple[str, str]]:
        """
        Returns distinct (project_id, dataset_id) available for the given GCP client
        """
        return set((ds.project, ds.dataset_id) for ds in self._list_datasets())
