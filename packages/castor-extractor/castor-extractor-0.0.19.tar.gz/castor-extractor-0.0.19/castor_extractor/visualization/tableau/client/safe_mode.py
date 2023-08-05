import logging
from typing import Dict, List

import tableauserverclient as TSC  # type: ignore

from ....utils import EntitiesType
from ..constants import SAFE_MODE_PAGE_SIZE
from ..entities import TableauEntity
from ..errors import TableauErrorCode
from ..types import PageReturn, ServerResponseError
from ..usage import compute_usage_views
from .client_utils import extract_entity

logger = logging.getLogger(__name__)


def _paginated_option(page_number: int) -> TSC.RequestOptions:
    """Set up the Paginated option for TSC.RequestOptions"""
    return TSC.RequestOptions(
        pagesize=SAFE_MODE_PAGE_SIZE, pagenumber=page_number
    )


def _next_usage_page(client, page_number: int) -> PageReturn:
    """
    Request views per page
    return Usages | ServerResponseError | TableauErrorCode
    """
    options = _paginated_option(page_number)
    try:
        all_usages_items, _ = client._server.views.get(options, usage=True)
        return all_usages_items, None

    except ServerResponseError as error:
        expected = TableauErrorCode.PAGE_NUMBER_NOT_FOUND
        if error.code == expected.value:
            return None, expected
        raise error

    except ServerResponseError as error:
        return None, error


def safe_mode_fetch_usage(client) -> EntitiesType:
    """
    Iterate throught each page
    Returns computed usages when page number is not found
    Log errors if ServerResponseError is return
    """
    list_usages: List[Dict] = []
    page_number: int = 0

    while True:
        page_number += 1
        usages, error = _next_usage_page(client, page_number)
        if error == TableauErrorCode.PAGE_NUMBER_NOT_FOUND:
            return compute_usage_views(list_usages)

        if error:
            logger.warning(error)
            client.errors.append(str(error))
            continue

        if not usages:
            continue

        new_usages = [
            extract_entity(usage, TableauEntity.USAGE) for usage in usages
        ]
        list_usages.extend(new_usages)
