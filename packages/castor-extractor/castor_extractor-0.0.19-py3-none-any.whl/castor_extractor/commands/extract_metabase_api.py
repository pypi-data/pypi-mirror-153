import logging
from argparse import ArgumentParser

from castor_extractor.visualization import metabase  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    parser.add_argument("-b", "--base-url", help="Metabase base url")
    parser.add_argument("-u", "--username", help="Metabase username")
    parser.add_argument("-p", "--password", help="Metabase password")

    parser.add_argument("-o", "--output", help="Directory to write to")

    args = parser.parse_args()

    client = metabase.ApiClient(
        base_url=args.base_url, username=args.username, password=args.password
    )

    metabase.extract_all(
        client,
        output_directory=args.output,
    )
