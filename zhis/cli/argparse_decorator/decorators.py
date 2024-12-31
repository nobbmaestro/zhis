import argparse
from typing import Any, Callable, Optional, Sequence, Union, overload

from .annotations import F


@overload
def command(
    name: str,
    *,
    parent: Optional[F] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    help: Optional[str] = None,  # pylint: disable=redefined-builtin
    metavar: Optional[str] = None,
    required: bool = False,
    **kwargs: Union[str, bool, Optional[Any]],
) -> Callable[[F], F]: ...


@overload
def argument(
    *name_or_flags: str,
    action: Optional[Union[str, argparse.Action]] = ...,
    nargs: Optional[Union[int, str]] = ...,
    const: Optional[Any] = ...,
    default: Optional[Any] = ...,
    type: Optional[Callable[[str], Any]] = ...,  # pylint: disable=redefined-builtin
    choices: Optional[Sequence[Any]] = ...,
    required: bool = ...,
    help: Optional[str] = ...,  # pylint: disable=redefined-builtin
    metavar: Optional[str] = ...,
    dest: Optional[str] = ...,
) -> Callable[[F], F]: ...


def command(
    *args: str,
    parent: Optional[F] = None,
    **kwargs: Any,
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        if parent:
            subcommands = getattr(parent, "__subcommands__", [])
            subcommands.append(func)
            setattr(parent, "__subcommands__", subcommands)
        setattr(func, "__command__", (args, kwargs))
        return func

    return decorator


def argument(
    *name_or_flags: str,
    **kwargs: Any,
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        arguments = getattr(func, "__arguments__", [])
        arguments.append((name_or_flags, kwargs))
        setattr(func, "__arguments__", arguments)
        return func

    return decorator
