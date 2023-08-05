from typing import Any, Callable, Dict, List, Mapping, Sequence, Union

EntitiesType = List[Dict]

# https://stackoverflow.com/questions/51291722/define-a-jsonable-type-using-mypy-pep-526
JsonType = Union[Sequence, Mapping, str, int, float, bool]

Callback = Callable[[Any], Any]
Getter = Union[str, Callback]
