#!/usr/bin/env python3
import json
import logging
import ntpath
from datetime import datetime
from typing import Iterable, Optional, Union
from uuid import UUID

from google.cloud import storage  # type: ignore

from .constant import BUCKETS, PATH_TEMPLATES, FileType
from .env import get_blob_env
from .utils import file_exist, iter_files

logger = logging.getLogger(__name__)


def _client(credentials: Union[str, dict]) -> storage.Client:
    """supports dict, string or path to the JSON file"""
    if isinstance(credentials, dict):
        return storage.Client.from_service_account_info(credentials)
    if file_exist(credentials):
        return storage.Client.from_service_account_json(credentials)
    if isinstance(credentials, str):
        credentials = json.loads(credentials)
        return storage.Client.from_service_account_info(credentials)
    raise ValueError("needs path or dict for credentials")


def _path(source_id: UUID, file_type: FileType, file_path: str) -> str:
    now = datetime.utcnow()
    timestamp = int(now.timestamp())
    filename = ntpath.basename(file_path)

    path_template = PATH_TEMPLATES[file_type]
    return path_template.format(
        timestamp=timestamp,
        source_id=source_id,
        filename=filename,
    )


def _get_blob(
    credentials: Union[str, dict],
    source_id: UUID,
    file_path: str,
    file_type: FileType,
) -> storage.Blob:
    """get the target blob to upload to"""
    client = _client(credentials)
    bucket_name = BUCKETS[file_type]
    path = _path(source_id, file_type, file_path)

    bucket = client.bucket(bucket_name)
    return bucket.blob(path)


def _upload(
    credentials: Union[str, dict],
    source_id: UUID,
    file_path: str,
    file_type: FileType,
) -> None:
    """
    credentials: path to file or dict
    source_id: id for the source
    file_type: type of file to upload
    file_path: path to the local file to upload
    """
    timeout, retries = get_blob_env()

    blob = _get_blob(credentials, source_id, file_path, file_type)
    with open(file_path, "rb") as f:
        blob.upload_from_file(f, timeout=timeout, num_retries=retries)
    logger.info(
        f"uploaded {file_path} as {file_type.value} to {blob.public_url}"
    )


def upload_manifest(
    credentials: Union[str, dict], source_id: UUID, file_path: str
) -> None:
    """
    credentials: path to file or dict
    source_id: id for the source
    file_path: path to the local manifest to upload
    """
    _upload(credentials, source_id, file_path, FileType.DBT)


def upload(
    credentials: Union[str, dict],
    source_id: UUID,
    file_type: FileType,
    file_path: Optional[str] = None,
    directory_path: Optional[str] = None,
) -> None:
    """
    credentials: path to file or dict
    source_id: id for the source
    file_type: type of file(s) uploaded - see FileType Enum
    file_path: path to the local visualization or warehouse file to upload
    directory_path: path to the local directory containing files to upload
    """
    files: Iterable[str]
    if directory_path:
        files = iter_files(directory_path)
    elif file_path:
        files = [file_path]
    else:
        message = "either file_path or directory_path should be defined"
        raise ValueError(message)

    for file_ in files:
        _upload(credentials, source_id, file_, file_type)
