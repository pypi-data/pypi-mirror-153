"""convert files to csv"""
import csv
import json
import sys
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import IO, Any, Iterable, Iterator, List, Sequence, Union
from uuid import UUID

ENCODING = "utf8"

CSV_OPTIONS = {
    "delimiter": ",",
    "quoting": csv.QUOTE_ALL,
    "quotechar": '"',
}

ScalarValue = Union[int, float, None, str]


def _header(row: dict) -> Sequence[str]:
    return [str(r) for r in row.keys()]


def _scalar(value: Any) -> ScalarValue:
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    # fallback
    return str(value)


def _row(header: Sequence[str], row: dict) -> List[ScalarValue]:
    return [_scalar(row.get(h)) for h in header]


def to_string_array(arr_json: str) -> List[str]:
    """
    Converts a JSON-serialized string array value as a string to a list
    Ex: '["items","count"]' to ["items", "order"]
    """

    if not arr_json.startswith("[") or not arr_json.endswith("]"):
        raise ValueError(f"Cannot deserialize (not an array): {arr_json}")

    try:
        array = json.loads(arr_json)
    except ValueError:
        raise ValueError(f"Cannot deserialize (not a JSON): {arr_json}")

    if not all(isinstance(el, str) for el in array):
        raise ValueError(f"Not an array of strings: {arr_json}")

    return array


def to_csv(buffer: IO[str], data: Iterable[dict]) -> bool:
    """convert data as list of dicts to CSV string"""

    writer = csv.writer(
        buffer,
        delimiter=CSV_OPTIONS["delimiter"],
        quoting=CSV_OPTIONS["quoting"],
        quotechar=CSV_OPTIONS["quotechar"],
    )
    header = None
    for row in data:
        # write header once
        if not header:
            header = _header(row)
            writer.writerow(header)
        converted = _row(header, row)
        writer.writerow(converted)
    return True


def from_csv(buffer: IO[str]) -> Iterator[dict]:
    """convert data as from a CSV string to list of dict"""
    try:
        reader = csv.reader(
            buffer,
            delimiter=CSV_OPTIONS["delimiter"],
            quoting=CSV_OPTIONS["quoting"],
            quotechar=CSV_OPTIONS["quotechar"],
        )
        header: List[str] = []
        for row in reader:
            if not header:
                header = list(row)
                continue
            yield {h: v for h, v in zip(header, row)}
    finally:
        # closing of the file must happen after all iterations
        buffer.close()


class Formatter(ABC):
    """
    Abstract class to Serialize/Deserialize to any format
    """

    @abstractmethod
    def extension(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def serialize(buffer: IO[str], data: Iterable[dict]) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data: IO[str]) -> Iterator[dict]:
        pass


class CsvFormatter(Formatter):
    """
    Serialize/Deserialize CSV
    """

    def extension(self) -> str:
        return "csv"

    # increase the size limit to its maximum (some fields are very large)
    csv.field_size_limit(sys.maxsize)

    @staticmethod
    def serialize(buffer: IO[str], data: Iterable[dict]) -> bool:
        return to_csv(buffer, data)

    @staticmethod
    def deserialize(buffer: IO[str]) -> Iterator[dict]:
        return from_csv(buffer)


class CustomEncoder(json.JSONEncoder):
    """supersedes the default encoder to handle additional types"""

    def default(self, obj: object) -> object:
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)


class JsonFormatter(Formatter):
    """
    Serialize/Deserialize JSON
    """

    def extension(self) -> str:
        return "json"

    @staticmethod
    def serialize(buffer: IO[str], data: Iterable[dict]) -> bool:
        try:
            json.dump(data, fp=buffer, cls=CustomEncoder)
            return True
        except ValueError:
            return False

    @staticmethod
    def deserialize(buffer: IO[str]) -> Iterator[dict]:
        try:
            data = json.load(buffer)
            return data
        finally:
            buffer.close()
