# type: ignore

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Sequence

from marshmallow import EXCLUDE
from textual.color import Color
from textual.message import Message
from textual.theme import Theme


class Column(Enum):
    EXIT_CODE = auto()
    EXECUTED_AT = auto()
    EXECUTED_IN = auto()
    TMUX_SESSION = auto()
    COMMAND = auto()
    PATH = auto()


class Mode(Enum):
    FULLSCREEN = 0
    INLINE = 1


@dataclass
class CustomTheme:
    primary: str = "#d5ced9"
    secondary: str = "#a0a1a7"
    accent: str = "#00e8c6"
    border: str = "#464949"
    background: str = "#23262e"

    @property
    def name(self) -> str:
        return "default"

    def to_theme(self) -> Theme:
        return Theme(
            name=self.name,
            accent=Color.parse(self.accent),
            background=Color.parse(self.background),
            foreground=Color.parse(self.primary),
            panel=Color.parse(self.border),
            primary=Color.parse(self.primary),
            secondary=Color.parse(self.secondary),
            surface=Color.parse(self.background),
        )


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
    theme: CustomTheme = field(default_factory=CustomTheme)

    class Meta:
        unknown = EXCLUDE


@dataclass
class SelectedCommandResponse(Message):
    command: str
