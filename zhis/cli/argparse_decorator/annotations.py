from argparse import Namespace
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

Command = Callable[[Namespace, Any], Any]
