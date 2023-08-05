from typing import Dict, Iterator, Optional

from ....utils import EntitiesType
from ..entities import EXPORTED_FIELDS, QUERY_FIELDS, TableauEntity

QUERY_TEMPLATE = """
{{
  {object_type}Connection(first: {page_size}, after: AFTER_TOKEN_SIGNAL) {{
    nodes {{ {query_fields}
    }}
    pageInfo {{
      hasNextPage
      endCursor
    }}
    totalCount
  }}
}}
"""

RESOURCE_TEMPLATE = "{resource}Connection"


def get_paginated_objects(
    server, entity: TableauEntity, page_size: int
) -> EntitiesType:

    fields = QUERY_FIELDS[entity]["fields"].value
    object_type = QUERY_FIELDS[entity]["object_type"].value
    query = QUERY_TEMPLATE.format(
        object_type=object_type,
        page_size=page_size,
        query_fields=fields,
    )
    resource = RESOURCE_TEMPLATE.format(resource=object_type)

    return [
        result
        for results in query_scroll(server, query, resource)
        for result in results
    ]


def query_scroll(server, query: str, resource: str) -> Iterator[EntitiesType]:
    """build a tableau query iterator handling pagination and cursor"""

    def _call(cursor: Optional[str]) -> dict:
        # If cursor is defined it must be quoted else use null token
        token = "null" if cursor is None else f'"{cursor}"'
        query_ = query.replace("AFTER_TOKEN_SIGNAL", token)

        return server.metadata.query(query_)["data"][resource]

    cursor = None
    while True:
        payload = _call(cursor)
        yield payload["nodes"]

        page_info = payload["pageInfo"]
        if page_info["hasNextPage"]:
            cursor = page_info["endCursor"]
        else:
            break


def extract_entity(entity: Dict, entity_type: TableauEntity) -> Dict:
    """Agnostic function extracting dedicated attributes with define entity"""
    return {key: getattr(entity, key) for key in EXPORTED_FIELDS[entity_type]}
