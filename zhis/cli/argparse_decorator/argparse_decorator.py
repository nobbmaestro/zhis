import argparse
from collections import defaultdict
from inspect import signature
from itertools import chain
from typing import Any, Callable, Optional, Sequence

import zhis

from .annotations import Command
from .formatters import CustomHelpFormatter


class ArgParseDecorator:
    def __init__(self):
        self.parser = None
        self.commands = []
        self.hooks = defaultdict(list)
        self.contexts = {}

    def add_command(self, func: Command):
        self.commands.append(func)

    def add_hook(
        self,
        callback: Callable[[argparse.Namespace], None],
        on_command: Optional[Callable] = None,
    ):
        key = on_command if on_command else "__any__"
        self.hooks[key].append(callback)

    def add_context(self, obj: Any):
        self.contexts[type(obj)] = obj

    def run(self, args=None):
        parser = self._create_parser(self.commands)

        parsed_args = parser.parse_args(args)

        for hook in chain(
            self.hooks["__any__"],
            self.hooks[parsed_args.func],
        ):
            hook(parsed_args)

        kwargs = {
            param.name: self.contexts.get(param.annotation, None)
            for param in signature(parsed_args.func).parameters.values()
            if param.annotation in self.contexts
        }

        parsed_args.func(parsed_args, **kwargs)

    @classmethod
    def _create_parser(cls, commands: Sequence[Callable]) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"%(prog)s {zhis.__version__}",
        )

        subparsers = parser.add_subparsers(
            title="commands",
            required=True,
            metavar="COMMAND",
        )
        for func in commands:
            cls._create_command(func, subparsers)

        return parser

    @classmethod
    def _create_command(cls, func, root_parser):
        args, kwargs = getattr(func, "__command__", ([], {}))

        parser = root_parser.add_parser(
            *args, **kwargs, formatter_class=CustomHelpFormatter
        )
        parser.set_defaults(func=func)

        for args, kwargs in getattr(func, "__arguments__", []):
            parser.add_argument(*args, **kwargs)

        if getattr(func, "__subcommands__", []):
            subparsers = parser.add_subparsers(
                title="commands",
                required=True,
                metavar="COMMAND",
            )
            for sub_func in getattr(func, "__subcommands__", []):
                cls._create_command(sub_func, subparsers)
