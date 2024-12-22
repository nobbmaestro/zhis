import datetime
import logging
from typing import List, Optional

from zhis.models import CliCommand, History, Path, TmuxSession


def register_command(
    command: List[str],
    session: str,
    path: str,
    last_execution: datetime.datetime = datetime.datetime.now(),
    exit_code: Optional[int] = None,
):
    cli_command, _ = CliCommand.get_or_create(command=" ".join(command))
    tmux_session, _ = TmuxSession.get_or_create(session=session)
    path, _ = Path.get_or_create(path=path)

    logging.debug(
        "Register command: %s, exit_code: %s, path: %s, tmux_session: %s",
        " ".join(command),
        exit_code,
        path,
        session,
    )

    History.create(
        command=cli_command,
        exit_code=exit_code,
        last_execution=last_execution,
        path=path,
        session=tmux_session,
    )
