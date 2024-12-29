import argparse
import logging
import os
import sys

from zhis.__version__ import __version__
from zhis.config import Config, load_config
from zhis.db import database_connection
from zhis.models import CliCommand, History
from zhis.ui.ui import ZshHistoryApp
from zhis.utils.helpers import get_current_tmux_session


def on_run_app_ui():
    app = ZshHistoryApp()
    return app.run()


def on_register_command(args, config: Config):
    return History.register_command(
        command=" ".join(args.cmd),
        exit_code=args.exit_code,
        path_context=args.path,
        session_context=args.tmux_session,
        exclude_commands=config.database.exclude_commands,
    )


def on_import_from_histfile_command(args, config: Config):
    if not os.path.isfile(args.filename):
        print("File does not exist")
        sys.exit(1)

    commands = []
    with open(args.filename, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            command = ""
            if line.startswith(": "):
                command = line.strip("\n").split(";")[-1]
            else:
                command = line.strip("\n")

            if command:
                commands.append(command)

    for command in commands:
        if CliCommand.get_or_none(command=command) is None:
            History.register_command(
                command=command,
                exclude_commands=config.database.exclude_commands,
            )


def on_search_command(args, config: Config):  # pylint: disable=unused-argument
    if args.previous:
        prev_command = History.get_previous_command(args.tmux_session)
        print(prev_command.command.command if prev_command else "")


def main():
    # Base parser to share common options like verbose
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="run in verbose mode",
    )

    # Main parser
    argparser = argparse.ArgumentParser(
        parents=[base_parser],
        description="Zsh History CLI",
    )
    argparser.add_argument(
        "--version",
        action="version",
        version=f"zhis {__version__}",
    )

    subparsers = argparser.add_subparsers(
        dest="command",
        required=False,
        title="commands",
    )

    # Register subcommand
    register_parser = subparsers.add_parser(
        "register",
        parents=[base_parser],
        help="Register a new command",
    )
    register_parser.add_argument(
        "cmd",
        nargs="*",
        help="Command to register",
    )
    register_parser.add_argument(
        "--exit-code",
        type=int,
        default=None,
        help="Exit code for the command",
    )
    register_parser.add_argument(
        "--path",
        default=os.getcwd(),
        help="Working directory context",
    )
    register_parser.add_argument(
        "--tmux-session",
        default=get_current_tmux_session(),
        help="Tmux session context",
    )
    register_parser.set_defaults(func=on_register_command)

    # Import subcommand
    import_parser = subparsers.add_parser(
        "import",
        parents=[base_parser],
        help="Import history file",
    )
    import_parser.add_argument(
        "filename",
        help="File to import",
    )
    import_parser.set_defaults(func=on_import_from_histfile_command)

    # Search subcommand
    search_parser = subparsers.add_parser(
        "search",
        parents=[base_parser],
        help="Search history",
    )
    search_parser.add_argument(
        "--previous",
        action="store_true",
        help="Retrieve the previous command",
    )
    search_parser.add_argument(
        "--tmux-session",
        default=get_current_tmux_session(),
        help="Tmux session context",
    )
    search_parser.set_defaults(func=on_search_command)

    args = argparser.parse_args()

    logging.basicConfig(
        level=logging.getLevelName(logging.INFO if args.verbose else logging.CRITICAL),
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )
    config = load_config()

    with database_connection():
        if args.command is None:
            on_run_app_ui()
        else:
            args.func(args, config)
