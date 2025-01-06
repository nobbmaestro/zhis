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


@history_command.command("list", help="List all items in history.")
@click.option(
    "-s",
    "--tmux-session",
    help="Filter search results by tmux session.",
)
@click.option(
    "-e",
    "--exit-code",
    type=int,
    help="Filter search results by exit code.",
)
@click.option(
    "-c",
    "--cwd",
    help="Filter search results by directory.",
)
@click.option(
    "-u",
    "--unique",
    is_flag=True,
    help="Filter search results by uniqueness.",
)
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def history_list_command(
    tmux_session: str,
    cwd: str,
    exit_code: int,
    unique: bool,
    verbose: bool,  # pylint: disable=unused-argument
):
    with database_connection():
        query = History.query_history(
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
        )
        query = query.select(History.command).distinct() if unique else query
        for cmd in query:
            click.echo(cmd.command)
