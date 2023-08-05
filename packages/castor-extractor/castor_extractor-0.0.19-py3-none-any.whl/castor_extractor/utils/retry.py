import logging
import random
import time
from enum import Enum
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union
from urllib.error import HTTPError

logger = logging.getLogger(__name__)


MS_IN_SEC = 1000


class RetryStrategy(Enum):
    """retry mechanism"""

    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


DEFAULT_STRATEGY = RetryStrategy.CONSTANT


class Retry:
    """handling retry check and wait"""

    def __init__(
        self,
        count: int,
        base_ms: int,
        jitter_ms: int,
        strategy: Optional[RetryStrategy] = None,
    ):
        self._max = count
        self._base = base_ms
        self._jitter = jitter_ms
        self._strategy = strategy or DEFAULT_STRATEGY
        self.count = 0

    def jitter(self) -> int:
        """compute random jitter in ms"""
        min_ = self._jitter // 2
        max_ = int(self._jitter * 1.5)
        return random.randrange(min_, max_)

    def base(self) -> int:
        """compute base wait time in ms"""
        base = self._base
        if self._strategy == RetryStrategy.CONSTANT:
            return base
        if self._strategy == RetryStrategy.LINEAR:
            return base * self.count
        # exponential
        scaled = float(base) / MS_IN_SEC
        return int(scaled ** self.count * MS_IN_SEC)

    def check(self) -> bool:
        """check wheter retry should happen or not"""
        if self.count >= self._max:
            return False
        self.count += 1
        wait_ms = self.base() + self.jitter()
        time.sleep(float(wait_ms) / MS_IN_SEC)
        return True


WrapperReturnType = Union[Tuple[BaseException, None], Tuple[None, Any]]


def retry(
    exceptions: Sequence[Type[BaseException]],
    count: int = 1,
    base_ms: int = 0,
    jitter_ms: int = 0,
    strategy: Optional[RetryStrategy] = None,
) -> Callable:
    """retry decorator"""

    exceptions_ = tuple(e for e in exceptions)

    def _wrapper(callable: Callable) -> Callable:
        def _try(*args, **kwargs) -> WrapperReturnType:
            try:
                return None, callable(*args, **kwargs)
            except exceptions_ as err:
                return err, None

        def _func(*args, **kwargs) -> Any:
            retry = Retry(count, base_ms, jitter_ms, strategy)
            while True:
                err, result = _try(*args, **kwargs)
                if err is None:
                    return result
                if retry.check():
                    logger.warning(f"retrying following: {err}")
                    continue
                raise err

        return _func

    return _wrapper
