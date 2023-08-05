import logging
from typing import Iterable, Tuple

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    validate_baseurl,
    write_json,
    write_summary,
)
from .api import ApiClient, Credentials, explore_names_associated_to_dashboards
from .entities import LookerEntity

BASE_URL = "CASTOR_LOOKER_BASE_URL"
CLIENT_ID = "CASTOR_LOOKER_CLIENT_ID"
CLIENT_SECRET = "CASTOR_LOOKER_CLIENT_SECRET"

logger = logging.getLogger(__name__)


def iterate_all_data(**kwargs: str) -> Iterable[Tuple[LookerEntity, list]]:
    """Iterate over the extracted Data From looker"""

    base_url = validate_baseurl(kwargs.get("base_url") or from_env(BASE_URL))
    client_id = kwargs.get("client_id") or from_env(CLIENT_ID)
    client_secret = kwargs.get("client_secret") or from_env(CLIENT_SECRET)

    client = ApiClient(
        credentials=Credentials(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    logger.info("Extracting users from Looker API")
    yield LookerEntity.USERS, deep_serialize(client.users())

    logger.info("Extracting folders from Looker API")
    yield LookerEntity.FOLDERS, deep_serialize(client.folders())

    logger.info("Extracting looks from Looker API")
    yield LookerEntity.LOOKS, deep_serialize(client.looks())

    logger.info("Extracting dashboards from Looker API")
    dashboards = client.dashboards()
    yield LookerEntity.DASHBOARDS, deep_serialize(dashboards)

    logger.info("Extracting lookml models from Looker API")
    lookmls = client.lookml_models()
    yield LookerEntity.LOOKML_MODELS, deep_serialize(lookmls)

    logger.info("Extracting explores from Looker API")
    explore_names = explore_names_associated_to_dashboards(lookmls, dashboards)
    yield LookerEntity.EXPLORES, deep_serialize(client.explores(explore_names))

    logger.info("Extracting connections from Looker API")
    connections = client.connections()
    yield LookerEntity.CONNECTIONS, deep_serialize(connections)

    logger.info("Extracting projects from Looker API")
    projects = client.projects()
    yield LookerEntity.PROJECTS, deep_serialize(projects)


def extract_all(**kwargs: str) -> None:
    """Extract Data From looker and store it locally in files under the output_directory"""
    output_directory = kwargs.get("output_directory") or from_env(OUTPUT_DIR)
    base_url = validate_baseurl(kwargs.get("base_url") or from_env(BASE_URL))

    ts = current_timestamp()

    for key, data in iterate_all_data(**kwargs):
        filename = get_output_filename(key.value, output_directory, ts)
        write_json(filename, data)

    write_summary(output_directory, ts, base_url=base_url)
