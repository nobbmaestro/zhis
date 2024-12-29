import logging
import os
import sys

import click

from zhis.db import database_connection
from zhis.models import CliCommand, History
from zhis.ui import ZshHistoryApp
from zhis.utils.helpers import get_current_tmux_session


@click.command(name="gui")
def run_gui_app():
    app = ZshHistoryApp()
    with database_connection():
        selected = app.run()
        click.echo(selected)


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


@click.command(name="import")
@click.argument("filename")
def import_histfile(filename):
    if not os.path.isfile(filename):
        click.echo("File does not exist")
        sys.exit(1)

    commands = []
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            command = ""
            if line.startswith(": "):
                command = line.strip("\n").split(";")[-1]
            else:
                command = line.strip("\n")

            if command:
                commands.append(command)

    with database_connection():
        for command in commands:
            if CliCommand.get_or_none(command=command) is None:
                History.register_command(
                    command=command,
                )


@click.command()
@click.option(
    "--previous",
    is_flag=True,
    help="",
)
@click.option(
    "--tmux-session",
    default=get_current_tmux_session(),
    help="tmux session context",
)
def search(previous, tmux_session):
    if previous:
        with database_connection():
            prev_command = History.get_previous_command(tmux_session)
            click.echo(prev_command.command.command if prev_command else "")


@click.group(invoke_without_command=True)
@click.version_option()
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        case_sensitive=True,
    ),
    default="CRITICAL",
)
@click.pass_context
def cli(ctx, log_level):
    logging.basicConfig(
        level=logging.getLevelName(log_level),
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )

    if ctx.invoked_subcommand is None:
        run_gui_app()


cli.add_command(register)
cli.add_command(search)
cli.add_command(import_histfile)
cli.add_command(run_gui_app)
