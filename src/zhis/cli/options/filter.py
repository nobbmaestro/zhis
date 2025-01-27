import click


def tmux_session_filter_option(func):
    return click.option(
        "-s",
        "--tmux-session",
        help="Filter search results by tmux session.",
    )(func)


def exit_code_filter_option(func):
    return click.option(
        "-e",
        "--exit-code",
        type=int,
        help="Filter search results by exit code.",
    )(func)


def cwd_filter_option(func):
    return click.option(
        "-c",
        "--cwd",
        help="Filter search results by directory.",
    )(func)


def unique_filter_option(func):
    return click.option(
        "-u",
        "--unique",
        is_flag=True,
        help="Filter search results by uniqueness.",
    )(func)
