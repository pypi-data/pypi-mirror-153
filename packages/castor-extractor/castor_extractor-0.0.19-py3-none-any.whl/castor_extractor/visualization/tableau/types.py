from typing import Dict, List, Tuple, Union

from tableauserverclient import ServerResponseError  # type: ignore
from typing_extensions import Literal

from .errors import TableauErrorCode

PageReturn = Union[
    Tuple[List[Dict], Literal[None]],
    Tuple[Literal[None], Union[TableauErrorCode, ServerResponseError]],
]
