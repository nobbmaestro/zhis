import logging

import click

from zhis.db import database_connection


@click.command()
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
@click.version_option()
def cli(verbose: bool):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.CRITICAL,
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )

    with database_connection():
        pass
