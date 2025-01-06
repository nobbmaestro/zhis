import os
from typing import List

import click

from zhis.db import History, database_connection
from zhis.utils.helpers import get_current_tmux_session


@click.group("history", help="Manipulate history database.")
def history_command():
    pass  # pylint: disable=unnecessary-pass


@history_command.command("add", help="Add to history.")
@click.argument("CMD", nargs=-1)
@click.option(
    "-s",
    "--tmux-session",
    default=get_current_tmux_session(),
    help="Tmux session context.",
)
@click.option(
    "-e",
    "--exit-code",
    type=int,
    default=None,
    help="Exit code for the command.",
)
@click.option(
    "-c",
    "--cwd",
    default=os.getcwd(),
    help="Working directory context.",
)
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def history_add_command(
    cmd: List[str],
    tmux_session: str,
    cwd: str,
    exit_code: int,
    verbose: bool,  # pylint: disable=unused-argument
):
    with database_connection():
        command = " ".join(cmd)
        History.register_command(
            command=command,
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
        )
