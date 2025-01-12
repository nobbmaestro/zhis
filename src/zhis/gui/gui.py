from typing import Callable, Dict, Optional, Sequence

import peewee
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import DataTable, Footer, Input, Static

from zhis.utils.helpers import humanize_timedelta

from .types import Column, GuiConfig, SelectedCommandResponse

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
    Column.EXECUTED_IN: lambda entry: entry.executed_in,
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


class FocusLockedQueryInput(Input):
    BINDINGS = [
        Binding("left", "cursor_left", "Move cursor left", show=False),
        Binding("right", "cursor_right", "Move cursor right", show=False),
        Binding("backspace", "delete_left", "Delete character left", show=False),
        Binding("home,ctrl+a", "home", "Go to start", show=False),
        Binding("end,ctrl+e", "end", "Go to end", show=False),
        Binding("delete", "delete_right", "Delete character right", show=False),
        Binding("ctrl+u", "delete_left_all", "Delete all to the left", show=False),
    ]

    @property
    def locked(self):
        return True

    def on_focus(self) -> None:
        if not self.locked:
            super().on_focus()

    def on_blur(self) -> None:
        if self.locked:
            self.focus()


class HistoryDataTable(DataTable):
    BINDINGS = []


class Gui(App):
    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=True, priority=True),
        Binding("ctrl+q,ctrl+c", "quit", "Quit", show=True, priority=True),
        Binding("down,ctrl+n", "cursor_down", "Down", show=True),
        Binding("up,ctrl+p", "cursor_up", "Up", show=True),
    ]

    CSS_PATH = "styles/main.tcss"

    ENABLE_COMMAND_PALETTE = False

    def __init__(
        self,
        config: GuiConfig,
        query_callback: Callable[[str], peewee.ModelSelect],
        version: str = "",
    ):
        super().__init__()
        self.config = config
        self.version = version
        self.table = None
        self.pattern = ""

        self.query_callback = query_callback
        self.update_rows()

    def compose(self) -> ComposeResult:
        yield HistoryDataTable(
            cursor_type="row",
            show_header=self.config.show_columns_header,
        )
        yield FocusLockedQueryInput(value=self.pattern)
        with Horizontal(classes="footer"):
            yield Footer(show_command_palette=False)
            yield Static(f"zhis {self.version}")

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
            self.query_callback(self.pattern),
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

    @on(Input.Changed)
    async def update_table_content(self, event: Input.Changed):
        if self.table is None:
            return

        if event.value != self.pattern:
            self.pattern = event.value
            self.update_rows()
            self.update_table()

    @on(Input.Submitted)
    def send_selected_command_and_exit(
        self, event: Input.Submitted
    ):  # pylint: disable=unused-argument
        command_idx = self.config.columns.index(Column.COMMAND)
        if self.table:
            selected_data = self.table.get_row_at(self.table.cursor_row)
            self.exit(SelectedCommandResponse(command=selected_data[command_idx]))
