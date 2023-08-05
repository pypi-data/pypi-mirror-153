import logging
from argparse import ArgumentParser

from castor_extractor.visualization import tableau  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    user_group = parser.add_mutually_exclusive_group(required=False)
    user_group.add_argument("-u", "--user", help="Tableau user")
    user_group.add_argument("-n", "--token-name", help="Tableau token name")

    password_group = parser.add_mutually_exclusive_group(required=False)
    password_group.add_argument("-p", "--password", help="Tableau password")
    password_group.add_argument("-t", "--token", help="Tableau token")

    parser.add_argument("-b", "--server-url", help="Tableau server url")
    parser.add_argument("-i", "--site-id", help="Tableau site ID")
    parser.add_argument(
        "-s", "--safe-mode", help="Tableau safe mode", action="store_true"
    )
    parser.add_argument("-o", "--output", help="Directory to write to")

    args = parser.parse_args()

    client = tableau.ApiClient(
        user=args.user,
        password=args.password,
        token_name=args.token_name,
        token=args.token,
        server_url=args.server_url,
        site_id=args.site_id,
        safe_mode=args.safe_mode,
    )

    client.login()

    tableau.extract_all(
        client,
        output_directory=args.output,
    )
