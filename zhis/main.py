import logging
from argparse import Namespace

from zhis.cli.argparse_decorator.argparse_decorator import ArgParseDecorator
from zhis.cli.commands import history_command, import_histfile_command, search_command
from zhis.config import load_config


def configure_logger(args: Namespace):
    logging.basicConfig(
        level=logging.getLevelName(logging.INFO if args.verbose else logging.CRITICAL),
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )


def main():
    handler = ArgParseDecorator()
    config = load_config()

    # Configure commands
    handler.add_command(history_command)
    handler.add_command(search_command)
    handler.add_command(import_histfile_command)

    # Configure hooks
    handler.add_hook(configure_logger)

    # Configure contexts
    handler.add_context(config)

    handler.run()
