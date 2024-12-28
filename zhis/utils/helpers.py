import shutil
import subprocess
from datetime import datetime
from typing import Sequence

import timeago

from zhis.models.models import History


def get_current_tmux_session() -> str:
    if shutil.which("tmux") is None:
        return ""

    return (
        subprocess.run(
            ["tmux", "display-message", "-p", "'#S'"],
            capture_output=True,
            check=False,
            text=True,
        )
        .stdout.strip()
        .strip("'")
    )


def format_history_to_data_table(list_of_history: Sequence[History]):
    header = [
        "Executed",
        "Command",
        "Exit Code",
        "Tmux Session",
        "Path",
    ]

    rows = [
        [
            timeago.format(history.executed_at, datetime.now()),
            getattr(history.command, "command", ""),
            history.exit_code,
            getattr(history.session_context, "session", ""),
            getattr(history.path_context, "path", ""),
        ]
        for history in list_of_history
    ]

    return [header] + rows
