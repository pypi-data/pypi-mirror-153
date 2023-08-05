import os

from .constant import (
    CASTOR_LOOKER_PAGE_SIZE,
    CASTOR_LOOKER_TIMEOUT_SECOND,
    DEFAULT_LOOKER_PAGE_SIZE,
    DEFAULT_LOOKER_TIMEOUT_SECOND,
)


def _int_env(key_env_name: str, default_value: int):
    value = os.environ.get(key_env_name, default_value)
    try:
        return int(value)
    except ValueError:
        return default_value


def page_size() -> int:
    """
    Either returns the page size parameter from env or from default value
    """
    return _int_env(
        key_env_name=CASTOR_LOOKER_PAGE_SIZE,
        default_value=DEFAULT_LOOKER_PAGE_SIZE,
    )


def timeout_second() -> int:
    """
    Either returns the timeout second parameter from env or from default value
    """
    return _int_env(
        key_env_name=CASTOR_LOOKER_TIMEOUT_SECOND,
        default_value=DEFAULT_LOOKER_TIMEOUT_SECOND,
    )
