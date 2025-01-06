import enum
from dataclasses import dataclass, field
from typing import Sequence

from marshmallow import EXCLUDE
from textual.message import Message


class Column(enum.Enum):
    EXIT_CODE = 0
    EXECUTED_AT = 1
    EXECUTED_IN = 2
    TMUX_SESSION = 3
    COMMAND = 4
    PATH = 5


@dataclass
class GuiConfig:
    columns: Sequence[Column] = field(
        default_factory=lambda: [
            Column.EXIT_CODE,
            Column.EXECUTED_AT,
            Column.COMMAND,
        ]
    )

    class Meta:
        unknown = EXCLUDE


@dataclass
class UserSelectedEvent(Message):
    selected_row: int


@dataclass
class SelectedCommandResponse(Message):
    command: str
