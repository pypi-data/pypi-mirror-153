from abc import ABC, abstractmethod
from typing import Iterator

from sqlalchemy import text
from sqlalchemy.engine import create_engine

from .query import ExtractionQuery


class AbstractWarehouseClient(ABC):
    """interface for the client to connect to the source"""

    def __init__(self, **credentials: dict):
        """init signature can vary"""
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def close(self) -> bool:
        pass

    @abstractmethod
    def execute(self, query: ExtractionQuery) -> Iterator[dict]:
        pass


class SqlalchemyClient(AbstractWarehouseClient, ABC):
    def __init__(self, credentials: dict):
        super().__init__(**credentials)
        self._uri = self._build_uri(credentials)
        self._options = self._engine_options(credentials)
        self._engine = create_engine(self._uri, **self._options)
        self._connection = None

    @abstractmethod
    def _build_uri(self, credentials: dict) -> str:
        pass

    @abstractmethod
    def _engine_options(self, credentials: dict) -> dict:
        pass

    def connect(self) -> bool:
        self._engine.connect()
        return True

    def execute(self, query: ExtractionQuery) -> Iterator[dict]:
        self.connect()
        proxy = self._engine.execute(text(query.statement), query.params)
        results = (dict(row) for row in proxy)
        self.close()
        return results

    def close(self) -> bool:
        self._engine.dispose()
        return True
