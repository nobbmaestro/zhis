import click

from zhis.cli.commands import history_command, import_command, search_command
from zhis.cli.options import verbose_option


@click.group()
@verbose_option
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = None


cli.add_command(history_command)
cli.add_command(import_command)
cli.add_command(search_command)
