import click

from zhis.config import Config, serialize_config
from zhis.config.config import DEFAULT_USER_CONFIG_PATH


def print_default_config(ctx, param, value):  # pylint: disable=unused-argument
    if not value:
        return

    config = serialize_config(config=Config())

    click.echo(config)
    ctx.exit()


def print_config_dir(ctx, param, value):  # pylint: disable=unused-argument
    if not value:
        return

    click.echo(DEFAULT_USER_CONFIG_PATH)
    ctx.exit()


def print_config_option(func):
    return click.option(
        "-c",
        "--config",
        callback=print_default_config,
        expose_value=False,
        is_flag=True,
        is_eager=True,
        help="Show the default config and exit.",
    )(func)


def print_config_dir_option(func):
    return click.option(
        "-C",
        "--config-dir",
        callback=print_config_dir,
        expose_value=False,
        is_flag=True,
        is_eager=True,
        help="Show the config directory and exit.",
    )(func)
