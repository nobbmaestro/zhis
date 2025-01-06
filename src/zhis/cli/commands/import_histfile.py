import os
import sys

import click

from zhis.config import Config
from zhis.db import History, database_connection


@click.command("import", help="Import history from histfile.")
@click.argument("HISTFILE")
@click.pass_obj
def import_command(
    config: Config,
    histfile: str,
):
    if not os.path.isfile(histfile):
        click.echo("File does not exist")
        sys.exit(1)

    commands = []
    with open(histfile, "r", encoding="utf-8", errors="ignore") as file:
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
            if History.get_or_none(command=command) is None:
                History.register_command(
                    command=command,
                    exclude_commands=config.db.exclude_commands,
                )
