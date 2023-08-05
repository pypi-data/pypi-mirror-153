from typing import Any, DefaultDict, Dict, List, Sequence

from .object import getproperty
from .type import Getter


def group_by(identifier: Getter, elements: Sequence) -> Dict[Any, List]:
    """Groups the elements by the given key"""
    groups: Dict[Any, List] = DefaultDict(list)
    for element in elements:
        key = getproperty(element, identifier)
        groups[key].append(element)

    return groups
