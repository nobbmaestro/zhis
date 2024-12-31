from zhis.cli.argparse_decorator.decorators import argument, command
from zhis.config import Config
from zhis.db import database_connection
from zhis.ui.ui import ZshHistoryApp


@command(
    "search",
    help="interactive history search",
    description="Interactive history search",
)
@argument(
    "QUERY",
    nargs="*",
    default=None,
    help="search command keyword(s)",
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
def search_command(args, config: Config):  # pylint: disable=unused-argument
    # FIXME: Inject the query into ZshHistoryApp
    with database_connection():
        pattern = " ".join(args.QUERY)

        app = ZshHistoryApp()
        app.pattern = pattern

        selected = app.run()
        print(selected if selected else "")
