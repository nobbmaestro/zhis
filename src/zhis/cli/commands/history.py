import os
from typing import List

import click

from zhis.config import Config
from zhis.db import History, database_connection
from zhis.utils.helpers import get_current_tmux_session

from ..options.filter import (
    cwd_filter_option,
    exit_code_filter_option,
    tmux_session_filter_option,
    unique_filter_option,
)


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
@click.option(
    "--id",
    "return_id",
    is_flag=True,
    help="Return id of the created history entry.",
)
@click.pass_obj
def history_add_command(
    config: Config,
    cmd: List[str],
    tmux_session: str,
    cwd: str,
    exit_code: int,
    return_id: bool,
):
    with database_connection():
        command = " ".join(cmd)
        history_id = History.register_command(
            command=command,
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
            exclude_commands=config.db.exclude_commands,
        )

    if return_id and history_id != -1:
        click.echo(history_id)


@history_command.command("edit", help="Edit history by ID.")
@click.argument("CMD_ID", nargs=1)
@click.option(
    "-s",
    "--tmux-session",
    default=None,
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
    default=None,
    help="Working directory context.",
)
@click.option(
    "-d",
    "--duration",
    default=None,
    type=int,
    help="Execution duration of the CMD in micro seconds.",
)
def history_edit_command(
    cmd_id: int,
    tmux_session: str,
    cwd: str,
    exit_code: int,
    duration: int,
):
    with database_connection():
        History.edit_command(
            command_id=cmd_id,
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
            executed_in=duration,
        )


@history_command.command("list", help="List all items in history.")
@unique_filter_option
@tmux_session_filter_option
@exit_code_filter_option
@cwd_filter_option
def history_list_command(
    tmux_session: str,
    cwd: str,
    exit_code: int,
    unique: bool,
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


@history_command.command("last", help="Show last command and exit.")
@tmux_session_filter_option
@exit_code_filter_option
@cwd_filter_option
def history_last_command(
    tmux_session: str,
    cwd: str,
    exit_code: int,
):
    with database_connection():
        prev_command = History.get_previous_command(
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
        )
        click.echo(prev_command.command if prev_command else "")
