import os
import sys

import click

from zhis.db import History, database_connection


@click.command("import", help="Import history from histfile.")
@click.argument("HISTFILE")
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def import_command(
    histfile: str,
    verbose: bool,  # pylint: disable=unused-argument
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
                History.register_command(command=command)
