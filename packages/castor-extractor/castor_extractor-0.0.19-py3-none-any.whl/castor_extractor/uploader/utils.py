import os
from typing import Iterator


def iter_files(repository_path: str) -> Iterator[str]:
    """
    Given a repository path yield all files in that repository
    """

    for file in os.listdir(repository_path):
        file_path = os.path.join(repository_path, file)

        if os.path.isfile(file_path):
            yield file_path


def file_exist(f_path: str) -> bool:
    """
    Check if a file exist
    """
    return os.path.exists(os.path.expanduser(f_path))
