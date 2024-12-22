import logging
import os

import click

from zhis.db import database_connection
from zhis.models import History
from zhis.utils.helpers import get_current_tmux_session


@click.command()
@click.argument(
    "CMD",
    type=str,
    nargs=-1,
)
@click.option(
    "--exit-code",
    default=None,
    help="command entry to register",
)
@click.option(
    "--path",
    default=os.getcwd(),
    help="working directory context",
)
@click.option(
    "--tmux-session",
    default=get_current_tmux_session(),
    help="tmux session context",
)
def register(cmd, exit_code, path, tmux_session):
    with database_connection():
        return History.register_command(
            command=" ".join(cmd),
            exit_code=exit_code,
            path_context=path,
            session_context=tmux_session,
        )


@click.group()
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


cli.add_command(register)
