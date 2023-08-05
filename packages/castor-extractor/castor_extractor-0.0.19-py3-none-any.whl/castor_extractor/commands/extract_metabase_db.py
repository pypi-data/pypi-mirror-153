import logging
from argparse import ArgumentParser

from castor_extractor.visualization import metabase  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    # mandatory
    parser.add_argument(
        "-H", "--host", help="Host name where the server is running"
    )
    parser.add_argument("-P", "--port", help="TCP/IP port number")
    parser.add_argument("-d", "--database", help="Database name")
    parser.add_argument("-s", "--schema", help="Schema name")
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument(
        "-k", "--encryption_secret_key", help="Encryption secret key"
    )

    parser.add_argument("-o", "--output", help="Directory to write to")

    args = parser.parse_args()

    client = metabase.DbClient(
        host=args.host,
        port=args.port,
        database=args.database,
        schema=args.schema,
        username=args.username,
        password=args.password,
        encryption_secret_key=args.encryption_secret_key,
    )

    metabase.extract_all(
        client,
        output_directory=args.output,
    )
