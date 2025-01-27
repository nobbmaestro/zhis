import click

from zhis.cli.commands import (
    history_command,
    import_command,
    init_command,
    search_command,
)
from zhis.cli.options import (
    print_config_dir_option,
    print_config_option,
    verbose_option,
)
from zhis.config import load_config


@click.group()
@verbose_option
@print_config_option
@print_config_dir_option
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = load_config()


cli.add_command(history_command)
cli.add_command(import_command)
cli.add_command(search_command)
cli.add_command(init_command)
