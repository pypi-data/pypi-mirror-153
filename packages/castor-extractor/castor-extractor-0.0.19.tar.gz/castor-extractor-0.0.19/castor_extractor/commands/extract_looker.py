import logging
from argparse import ArgumentParser

from castor_extractor.visualization import looker  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()
    parser.add_argument("-b", "--base-url", help="Looker base url")
    parser.add_argument("-u", "--username", help="Looker client id")
    parser.add_argument("-p", "--password", help="Looker client secret")
    parser.add_argument("-o", "--output", help="Directory to write to")

    args = parser.parse_args()

    looker.extract_all(
        base_url=args.base_url,
        client_id=args.username,
        client_secret=args.password,
        output_directory=args.output,
    )
