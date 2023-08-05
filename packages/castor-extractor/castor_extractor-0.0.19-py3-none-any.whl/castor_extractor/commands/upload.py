import argparse
import logging

from castor_extractor.uploader import FileType  # type: ignore
from castor_extractor.uploader import upload  # type: ignore
from castor_extractor.uploader import upload_manifest  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--credentials",
        required=True,
        help="""Path to credentials or credentials as string""",
    )
    parser.add_argument(
        "-s", "--source_id", required=True, help="source id provided by castor"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file_path", help="path to file to upload")
    group.add_argument(
        "-d",
        "--directory_path",
        help="""directory containing the files to upload.
                WARNING: it will upload all the files included
                in the given repository.""",
    )
    supported_file_type = [ft.value for ft in FileType]
    parser.add_argument(
        "-t",
        "--file_type",
        help="type of file to upload, currently supported are {}".format(
            supported_file_type
        ),
        choices=supported_file_type,
    )
    parsed = parser.parse_args()
    return {
        "credentials": parsed.credentials,
        "source_id": parsed.source_id,
        "file_path": parsed.file_path,
        "directory_path": parsed.directory_path,
        "file_type": FileType(parsed.file_type),
    }


def main():
    params = _args()

    file_type = params.get("file_type")
    if file_type in [FileType.VIZ, FileType.WAREHOUSE]:
        upload(**params)

    if file_type == FileType.DBT:
        dir_path = params.pop("directory_path")
        assert not dir_path
        del params["file_type"]
        upload_manifest(**params)
