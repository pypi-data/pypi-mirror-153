import logging
from typing import Dict, List, Optional, cast

import requests

from ....utils import retry
from ..entities import (
    ENTITIES_WITH_OWNER,
    EXPORTED_FIELDS,
    ModeAnalyticsEntity as Entity,
)
from ..errors import (
    MissingPrerequisiteError,
    UnexpectedApiResponseError,
    check_errors,
)
from .constants import (
    CLIENT_NAME,
    RETRY_BASE_MS,
    RETRY_COUNT,
    RETRY_EXCEPTIONS,
    RETRY_JITTER_MS,
    RETRY_STRATEGY,
)
from .credentials import Credentials, CredentialsKey, get_value

logger = logging.getLogger(__name__)

URL_TEMPLATE = "{host}/api"

RawData = List[Dict]
Tokens = Optional[List[str]]


class Client:
    """
    Connect to Mode Analytics API and fetch main entities.
    https://mode.com/developer/api-reference/introduction/
    """

    def __init__(
        self,
        **kwargs,
    ):
        self._credentials = Credentials(
            host=get_value(CredentialsKey.HOST, kwargs).rstrip("/"),
            workspace=get_value(CredentialsKey.WORKSPACE, kwargs),
            token=get_value(CredentialsKey.TOKEN, kwargs),
            secret=get_value(CredentialsKey.SECRET, kwargs),
        )
        self._session = requests.Session()
        if not kwargs.get("no_checks"):
            self._check_connection()

    def _check_connection(self):
        authentication = self._credentials.authentication()
        url = self._url(with_workspace=False) + "/account"
        response = self._session.get(url, auth=authentication)
        self._handle_response(response)
        logger.info("Authentication succeeded.")

    @staticmethod
    def name() -> str:
        """return the name of the client"""
        return CLIENT_NAME

    @staticmethod
    def _handle_response(
        response: requests.Response,
        *,
        resource_name: Optional[str] = None,
    ) -> RawData:
        check_errors(response)
        result = response.json()

        if "_embedded" not in result:
            # some calls return data directly
            return result

        # most of calls return data in ["_embedded"]["resource_name"] node
        try:
            embedded = cast(Dict, result["_embedded"])
            return cast(List, embedded[resource_name])
        except (ValueError, KeyError):
            raise UnexpectedApiResponseError(resource_name, result)

    def base_url(self) -> str:
        """Return base_url from credentials"""
        return f"{self._credentials.host}/{self._credentials.workspace}"

    def _url(
        self,
        with_workspace: bool = True,
        space: Optional[str] = None,
        report: Optional[str] = None,
        resource_name: Optional[str] = None,
    ) -> str:
        url = URL_TEMPLATE.format(host=self._credentials.host)
        if with_workspace:
            url += f"/{self._credentials.workspace}"
        if space:
            url += f"/spaces/{space}"
        if report:
            url += f"/reports/{report}"
        if resource_name:
            url += f"/{resource_name}"
        return url

    @retry(
        exceptions=RETRY_EXCEPTIONS,
        count=RETRY_COUNT,
        base_ms=RETRY_BASE_MS,
        jitter_ms=RETRY_JITTER_MS,
        strategy=RETRY_STRATEGY,
    )
    def _call(
        self,
        *,
        with_workspace: bool = True,
        space: Optional[str] = None,
        report: Optional[str] = None,
        resource_name: Optional[str] = None,
    ) -> RawData:
        authentication = self._credentials.authentication()
        url = self._url(with_workspace, space, report, resource_name)
        logger.info(f"Calling {url}")
        response = self._session.get(url, auth=authentication)
        return self._handle_response(response, resource_name=resource_name)

    def _reports(self, spaces: Optional[RawData]) -> RawData:
        reports: RawData = []
        # the only way to fetch reports is to loop on spaces
        # https://mode.com/developer/api-reference/analytics/reports/#listReportsInSpace
        if not spaces:
            raise MissingPrerequisiteError(
                fetched=Entity.REPORT,
                missing=Entity.COLLECTION,
            )
        for space in spaces:
            space_token = space["token"]
            # example: https://modeanalytics.com/api/{workspace}/spaces/{space_token}/reports
            result = self._call(space=space_token, resource_name="reports")
            reports.extend(result)
        return reports

    def _queries(self, reports: Optional[RawData]) -> RawData:
        queries: RawData = []
        if not reports:
            raise MissingPrerequisiteError(
                fetched=Entity.QUERY,
                missing=Entity.REPORT,
            )
        for report in reports:
            report_token = report["token"]
            result = self._call(report=report_token, resource_name="queries")
            for query in result:
                query["report_token"] = report_token
            queries.extend(result)
        return queries

    def _members(self) -> RawData:
        members: RawData = []
        # the only way to fetch members is to loop on memberships
        # https://mode.com/developer/api-reference/management/workspace-memberships/#listMemberships
        memberships = self._call(resource_name="memberships")
        for mb in memberships:
            # then we fetch users one by one, using their {username}
            # why without workspace? because users can belong to several companies
            # example: https://modeanalytics.com/api/john_doe
            result = self._call(
                resource_name=mb["member_username"], with_workspace=False
            )
            members.append(cast(Dict, result))
        return members

    @staticmethod
    def _post_processing(entity: Entity, data: RawData) -> RawData:
        filtered = []
        for row in data:
            if entity in ENTITIES_WITH_OWNER:
                # extract creator from _links
                creator_href = row["_links"]["creator"]["href"]
                # remove "api/" to keep only the username
                row["creator"] = creator_href[5:]
            # keep only exported fields
            new = {key: row.get(key) for key in EXPORTED_FIELDS[entity]}
            filtered.append(new)
        return filtered

    def fetch(
        self,
        entity: Entity,
        *,
        additional_data: Optional[RawData] = None,
    ) -> RawData:
        """
        Fetch the given entity.

        :additional_data must be provided in certain cases
        - to fetch REPORTS, provide the list of COLLECTIONS
        - to fetch QUERIES, provide the list of REPORTS
        Otherwise MissingPrerequisiteError will be raised.

        It means that extracting all data must be executed in a certain order:
        ```
          members = client.fetch(Entity.MEMBER)
          datasources = client.fetch(Entity.DATASOURCE)
          collections = client.fetch(Entity.COLLECTION)
          reports = client.fetch(Entity.REPORT, additional_data=collections)
          queries = client.fetch(Entity.QUERY, additional_data=reports)
        ```
        """
        logger.info(f"Starting extraction for {entity.name}...")
        # specific calls
        if entity == Entity.REPORT:
            result = self._reports(spaces=additional_data)
        elif entity == Entity.MEMBER:
            result = self._members()
        elif entity == Entity.QUERY:
            result = self._queries(reports=additional_data)
        else:
            # generic calls
            # example: https://modeanalytics.com/api/{workspace}/spaces
            # example: https://modeanalytics.com/api/{workspace}/data_sources
            result = self._call(resource_name=entity.value)
        logger.info(f"{len(result)} rows extracted")
        return self._post_processing(entity, result)
