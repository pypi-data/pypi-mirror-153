"""
The Looker sdk only support configuration through file stored on the disk
This is an attempt to bypass this and configure the sdk using a config dict.
"""

from typing import Any, Dict, Optional

from looker_sdk.rtl import (
    auth_session,
    requests_transport,
    serialize,
    transport,
)
from looker_sdk.sdk import constants
from looker_sdk.sdk.api40 import methods as methods40
from looker_sdk.sdk.api40.models import (
    Dashboard,
    DashboardElement,
    DBConnection,
    Folder,
    Look,
    LookmlModel,
    LookmlModelExplore,
    LookmlModelExploreField,
    LookmlModelExploreFieldset,
    LookmlModelExploreJoins,
    LookmlModelNavExplore,
    Project,
    Query,
    User,
)
from typing_extensions import Protocol

from ..env import timeout_second


class Credentials:
    """ValueObject for the credentials"""

    def __init__(
        self,
        *,
        base_url: str,
        client_id: str,
        client_secret: str,
        timeout: Optional[int] = None,
        **_kwargs,
    ):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout: int = timeout or timeout_second()

    def to_dict(self) -> Dict[str, Any]:
        attrs = ("base_url", "client_id", "client_secret", "timeout")
        return {attr: getattr(self, attr) for attr in attrs}


def init40(config: Credentials) -> methods40.Looker40SDK:
    """Default dependency configuration"""
    settings = ApiSettings(config=config, sdk_version=constants.sdk_version)
    settings.is_configured()
    transport = requests_transport.RequestsTransport.configure(settings)
    return methods40.Looker40SDK(
        auth_session.AuthSession(
            settings,
            transport,
            serialize.deserialize40,
            "4.0",
        ),
        serialize.deserialize40,
        serialize.serialize,
        transport,
        "4.0",
    )


class CastorApiSettings(transport.PTransportSettings, Protocol):
    """This is an intermediate class that is meant to be extended (for typing purpose)"""

    def read_config(self) -> Dict[str, Any]:
        raise NotImplementedError()


class ApiSettings(CastorApiSettings):
    """SDK settings with initialisation using a credential object instead of a path to a .ini file"""

    def __init__(self, config: Credentials, sdk_version: Optional[str] = ""):
        """Configure using a config dict"""
        self.config = config.to_dict()
        self.verify_ssl = True
        self.base_url = self.config.get("base_url", "")
        self.timeout = config.timeout
        self.headers = {"Content-Type": "application/json"}
        self.agent_tag = f"{transport.AGENT_PREFIX}"
        if sdk_version:
            self.agent_tag += f" {sdk_version}"

    def read_config(self) -> Dict[str, Any]:
        """Returns a serialization of the credentials"""
        return self.config
