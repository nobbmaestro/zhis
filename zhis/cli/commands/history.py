import os
from argparse import Namespace

from zhis.cli.argparse_decorator.decorators import argument, command
from zhis.config import Config
from zhis.db import database_connection
from zhis.models import History
from zhis.utils.helpers import get_current_tmux_session


@command(
    "history",
    help="manipulate history database",
    description="Manipulate history database",
)
def history_command(args: Namespace, config: Config):  # pylint: disable=unused-argument
    pass


@command(
    "add",
    parent=history_command,
    help="add to history",
    description="Add to history",
)
@argument(
    "CMD",
    nargs="+",
    help="command to add",
)
@argument(
    "-s",
    "--tmux-session",
    default=get_current_tmux_session(),
    help="tmux session context",
)
@argument(
    "-e",
    "--exit",
    type=int,
    default=None,
    help="exit code for the command",
)
@argument(
    "-c",
    "--cwd",
    default=os.getcwd(),
    help="working directory context",
)
@argument(
    "-v",
    "--verbose",
    action="store_true",
    help="run in verbose mode",
)
def history_add_command(
    args: Namespace, config: Config
):  # pylint: disable=unused-argument
    with database_connection():
        return History.register_command(
            command=" ".join(args.CMD),
            exit_code=args.exit,
            path_context=args.path,
            session_context=args.tmux_session,
            exclude_commands=config.database.exclude_commands,
        )


@command(
    "last",
    parent=history_command,
    help="get last command and exit",
    description="Get last command and exit",
)
@argument(
    "-s",
    "--tmux-session",
    help="filter search results by tmux session",
)
@argument(
    "-c",
    "--cwd",
    help="filter search results by directory",
)
@argument(
    "-e",
    "--exit",
    type=int,
    help="filter search results by exit code",
)
@argument(
    "-v",
    "--verbose",
    action="store_true",
    help="run in verbose mode",
)
def history_last_command(args: Namespace):
    with database_connection():
        prev_command = History.get_previous_command(args.tmux_session)
        print(prev_command.command.command if prev_command else "")
