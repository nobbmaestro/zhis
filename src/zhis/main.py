import logging

import click

from zhis.cli.commands import history_command, import_command


def configure_logger(verbose: bool):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.CRITICAL,
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
@click.version_option()
def cli(verbose: bool):
    configure_logger(verbose)


cli.add_command(history_command)
cli.add_command(import_command)
