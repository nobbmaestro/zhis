import argparse
import os
import sys

from zhis.cli.argparse_decorator.decorators import argument, command
from zhis.config import Config
from zhis.db import database_connection
from zhis.models import CliCommand, History


@command(
    "import",
    help="import history file",
    description="Import history file",
)
@argument(
    "FILENAME",
    help="file to import",
)
@argument(
    "-v",
    "--verbose",
    action="store_true",
    help="run in verbose mode",
)
def import_histfile_command(args: argparse.Namespace, config: Config):
    if not os.path.isfile(args.FILENAME):
        print("File does not exist")
        sys.exit(1)

    history = []
    with open(args.FILENAME, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            entry = ""
            if line.startswith(": "):
                entry = line.strip("\n").split(";")[-1]
            else:
                entry = line.strip("\n")

            if entry:
                history.append(entry)

    with database_connection():
        for entry in history:
            if CliCommand.get_or_none(command=entry) is None:
                History.register_command(
                    command=entry,
                    exclude_commands=config.database.exclude_commands,
                )
