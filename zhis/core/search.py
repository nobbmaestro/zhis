from zhis.models import History, TmuxSession


def get_previous_command(tmux_session_context: str = "") -> "str":
    query = History.select().order_by(History.last_execution.desc())

    if tmux_session_context:
        tmux_session_id = TmuxSession.get_or_none(session=tmux_session_context)
        query = query.where(History.session == tmux_session_id)

    prev_command = query.first()

    return prev_command.command.command if prev_command else ""
