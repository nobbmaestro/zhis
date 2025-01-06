from typing import Callable, Dict, Optional, Sequence

import peewee
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Input, Static

from zhis.__version__ import __version__
from zhis.db import History
from zhis.utils.helpers import humanize_timedelta

from .types import Column, GuiConfig, SelectedCommandResponse, UserSelectedEvent

COLUMN_TO_NAME_MAP: Dict[Column, str] = {
    Column.EXIT_CODE: "Exit",
    Column.EXECUTED_AT: "Executed",
    Column.EXECUTED_IN: "Duration",
    Column.TMUX_SESSION: "Tmux Session",
    Column.COMMAND: "Command",
    Column.PATH: "Path",
}


COLUMN_TO_FIELD_OBTAIN_MAP: Dict[Column, Callable] = {
    Column.EXIT_CODE: lambda entry: entry.exit_code,
    Column.EXECUTED_AT: lambda entry: humanize_timedelta(entry.executed_at),
    Column.EXECUTED_IN: lambda entry: humanize_timedelta(entry.executed_in),
    Column.TMUX_SESSION: lambda entry: getattr(entry.session_context, "session", ""),
    Column.COMMAND: lambda entry: entry.command,
    Column.PATH: lambda entry: getattr(entry.path_context, "path", ""),
}


def format_history_to_data_table(
    history: peewee.ModelSelect,
    columns: Sequence[Column],
    names_map: Optional[Dict[Column, str]] = None,
    action_map: Optional[Dict[Column, Callable]] = None,
):
    names_map = names_map if names_map is not None else COLUMN_TO_NAME_MAP
    action_map = action_map if action_map is not None else COLUMN_TO_FIELD_OBTAIN_MAP

    header = [names_map.get(column, "") for column in columns]
    rows = [
        [action_map[column](entry) for column in columns] for entry in list(history)
    ]

    return [header] + rows


class HistoryDataTable(DataTable):
    BINDINGS = [
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
        ("enter", "select_cursor", "Select"),
    ]

    def action_select_cursor(self) -> None:
        selected_row = self.cursor_row
        self.post_message(UserSelectedEvent(selected_row=selected_row))


class Gui(App):

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+j", "cursor_down", "Down"),
        ("ctrl+k", "cursor_up", "Up"),
        ("?", "keybindings", "keybindings"),
    ]

    CSS = """
    Screen {
        layout: vertical;
    }

    Static {
        height: 2.5%;
    }

    DataTable {
        height: 1fr;
        border: round;
    }

    Input {
        max-height: 3;
        border: round;
    }

    Footer {
        height: 2.5%;
    }
    """

    def __init__(
        self,
        history: peewee.ModelSelect,
        config: GuiConfig,
    ):
        super().__init__()
        self.config = config
        self.history = history
        self.table = None
        self.pattern = ""

        self.update_rows()

    def compose(self) -> ComposeResult:
        yield Static(f"Zhis {__version__}")
        yield HistoryDataTable(cursor_type="row")
        yield Input(value=self.pattern, placeholder="Type your command here...")
        yield Footer()

    def on_mount(self) -> None:
        self.table = self.query_one(DataTable)
        self.update_table()

        # Set focus to the Input widget
        input_widget = self.query_one(Input)
        self.set_focus(input_widget)

    def update_table(self) -> None:
        if self.table is None:
            return

        if not self.table.columns:
            self.table.add_columns(*self.rows[0])

        if self.rows:
            self.table.clear()
            self.table.add_rows(self.rows[1:])

    def update_rows(self):
        self.rows = format_history_to_data_table(
            History.query_history(
                pattern=self.pattern,
                base_query=self.history,
            ),
            self.config.columns,
        )

    def action_cursor_up(self):
        if self.table is None:
            return
        self.table.action_cursor_up()

    def action_cursor_down(self):
        if self.table is None:
            return
        self.table.action_cursor_down()

    def on_input_changed(self, event: Input.Changed):
        if self.table is None:
            return

        if event.value != self.pattern:
            self.pattern = event.value
            self.update_rows()
            self.update_table()

    async def on_user_selection(self, event: UserSelectedEvent):
        command_idx = self.config.columns.index(Column.COMMAND)
        if self.table:
            selected_data = self.table.get_row_at(event.selected_row)
            self.exit(SelectedCommandResponse(command=selected_data[command_idx]))
