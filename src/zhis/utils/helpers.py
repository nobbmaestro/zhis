import datetime
import shutil
import subprocess


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


def humanize_timedelta(
    timestamp: datetime.datetime,
    baseline=datetime.datetime.now(),
):
    if timestamp is None or baseline is None:
        return ""

    delta = baseline - timestamp
    d_seconds = delta.total_seconds()

    units = [
        ("y", 60 * 60 * 24 * 365),
        ("w", 60 * 60 * 24 * 7),
        ("d", 60 * 60 * 24),
        ("h", 60 * 60),
        ("m", 60),
        ("s", 1),
    ]

    for unit, duration in units:
        if d_seconds >= duration:
            return f"{int(d_seconds//duration)}{unit} ago"

    return "just now"
