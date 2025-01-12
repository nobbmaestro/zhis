# type: ignore

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Sequence

from marshmallow import EXCLUDE
from textual.message import Message


class Column(Enum):
    EXIT_CODE = auto()
    EXECUTED_AT = auto()
    EXECUTED_IN = auto()
    TMUX_SESSION = auto()
    COMMAND = auto()
    PATH = auto()


@dataclass
class GuiConfig:
    columns: Sequence[Column] = field(
        default_factory=lambda: [
            Column.EXIT_CODE,
            Column.EXECUTED_AT,
            Column.COMMAND,
        ]
    )
    show_columns_header: bool = True

    class Meta:
        unknown = EXCLUDE


@dataclass
class SelectedCommandResponse(Message):
    command: str
