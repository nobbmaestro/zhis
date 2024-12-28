from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import DataTable, Footer, Input, Static

from zhis.__version__ import __version__
from zhis.models.models import History
from zhis.utils.helpers import format_history_to_data_table


@dataclass
class SelectedCommand(Message):
    command: str


class HistoryDataTable(DataTable):
    BINDINGS = [
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
        ("enter", "select_cursor", "Select"),
    ]

    def action_select_cursor(self) -> None:
        selected_row = self.cursor_row
        selected_data = self.get_row_at(selected_row)

        self.post_message(SelectedCommand(command=selected_data[1]))


class ZshHistoryApp(App):

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

    def __init__(self):
        super().__init__()
        self.table = None
        self.pattern = ""

    def compose(self) -> ComposeResult:
        yield Static(f"Zhis {__version__}")
        yield HistoryDataTable(cursor_type="row")
        yield Input(placeholder="Type your command here...")
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

        rows = format_history_to_data_table(
            History.query_history(
                pattern=self.pattern,
            )
        )

        if not self.table.columns:
            self.table.add_columns(*rows[0])

        if rows:
            self.table.clear()
            self.table.add_rows(rows[1:])

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

        self.pattern = event.value
        self.update_table()

    async def on_selected_command(self, event: SelectedCommand):
        self.exit(event.command)
