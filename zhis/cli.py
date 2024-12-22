import logging

import click

from zhis.db import database_connection


@click.command()
@click.version_option()
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        case_sensitive=True,
    ),
    default="CRITICAL",
)
def cli(log_level):
    logging.basicConfig(
        level=logging.getLevelName(log_level),
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )

    with database_connection():
        pass
