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
