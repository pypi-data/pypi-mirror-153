import logging
from argparse import ArgumentParser

from castor_extractor.warehouse import snowflake  # type: ignore

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main():
    parser = ArgumentParser()

    parser.add_argument("-a", "--account", help="Snowflake account")
    parser.add_argument("-u", "--user", help="Snowflake user")
    parser.add_argument("-p", "--password", help="Snowflake password")

    parser.add_argument(
        "--warehouse", help="Use a specific WAREHOUSE to run extraction queries"
    )
    parser.add_argument(
        "--role", help="Use a specific ROLE to run extraction queries"
    )

    parser.add_argument(
        "--db-allowed",
        nargs="*",
        help="List of databases that should be extracted",
    )
    parser.add_argument(
        "--db-blocked",
        nargs="*",
        help="List of databases that should not be extracted",
    )
    parser.add_argument(
        "--fetch-transient",
        action="store_true",
        help="Optional: will fetch transients tables if added",
    )

    parser.add_argument("-o", "--output", help="Directory to write to")

    parser.add_argument(
        "--skip-existing",
        dest="skip_existing",
        action="store_true",
        help="Skips files already extracted instead of replacing them",
    )
    parser.set_defaults(skip_existing=False)

    args = parser.parse_args()

    snowflake.extract_all(
        account=args.account,
        user=args.user,
        password=args.password,
        db_allowed=args.db_allowed,
        db_blocked=args.db_blocked,
        output_directory=args.output,
        skip_existing=args.skip_existing,
        fetch_transient=args.fetch_transient,
    )
