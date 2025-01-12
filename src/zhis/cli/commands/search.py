from functools import partial
from typing import List

import click

from zhis.__version__ import __version__
from zhis.config import Config
from zhis.db import History, database_connection
from zhis.gui import Gui, SelectedCommandResponse

from ..options.filter import (
    cwd_filter_option,
    exit_code_filter_option,
    tmux_session_filter_option,
)


@click.command("search", help="Interactive history search.")
@click.argument("KEYWORDS", nargs=-1)
@tmux_session_filter_option
@exit_code_filter_option
@cwd_filter_option
@click.pass_obj
def search_command(
    config: Config,
    keywords: List[str],
    tmux_session: str,
    cwd: str,
    exit_code: int,
):
    with database_connection():
        pattern = " ".join(keywords)

        query = History.query_history(
            pattern=pattern,
            tmux_session_context=tmux_session,
            path_context=cwd,
            exit_code=exit_code,
        )

        response = Gui(
            config.gui,
            query_callback=partial(History.query_history, base_query=query),
            version=__version__,
        ).run()

        if isinstance(response, SelectedCommandResponse):
            click.echo(response.command)
