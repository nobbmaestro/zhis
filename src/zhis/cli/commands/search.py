from typing import List

import click

from zhis.db import History, database_connection
from zhis.gui import Gui, GuiConfig, SelectedCommandResponse


@click.command("search", help="Interactive history search.")
@click.argument("KEYWORDS", nargs=-1)
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
@click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
def search_command(
    keywords: List[str],
    tmux_session: str,
    cwd: str,
    exit_code: int,
    verbose: bool,  # pylint: disable=unused-argument
):
    with database_connection():
        pattern = " ".join(keywords)

        query = History.query_history(
            pattern=pattern,
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
        )

        config = GuiConfig()
        response = Gui(query, config).run()

        if isinstance(response, SelectedCommandResponse):
            click.echo(response.command)
