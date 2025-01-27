# User Config

Default path for the global config file:

- `~/.config/zhis/config.yml`

## Default

```yml
# Config relating to the database
db:
  # List of regex for excluding commands
  # See https://github.com/nobbmaestro/zhis/blob/master/docs/config.md#exclude-commands-from-database
  exclude_commands: []

# Config relating to the GUI
gui:
  # Run GUI in FULLSCREEN or INLINE mode
  # See https://github.com/nobbmaestro/zhis/blob/master/docs/config.md#gui-mode
  mode: FULLSCREEN

  # List of GUI Columns
  # See https://github.com/nobbmaestro/zhis/blob/master/docs/config.md#gui-columns
  columns:
    - EXIT_CODE
    - EXECUTED_AT
    - COMMAND

  # If true, show the columns header in the GUI
  show_columns_header: true

  # Config relating to theme of the GUI
  # See https://github.com/nobbmaestro/zhis/blob/master/docs/config.md#theme-attributes
  theme:
    accent: "#00e8c6"
    background: "#23262e"
    border: "#464949"
    primary: "#d5ced9"
    secondary: "#a0a1a7"
```

## Exclude Commands from Database

In case you want to exclude commands by pattern, you can use `exclude_commands` for listing custom regex expressions.

Example:

```yml
db:
  exclude_commands:
    - ^clear
    - ^nvim
    - ^ls\s*$
```

## GUI Mode

If you don't like default `FULLSCREEN`, you can use `mode` modifier to alter the default mode.

Available modes:

| Mode       | Description                   |
| ---------- | ----------------------------- |
| FULLSCREEN | Runs GUI in fullscreen mode   |
| INLINE     | Runs GUI in inline shell mode |

## GUI Columns

`zhis` is storing various metadata associated to the stored command in the database.
However, this metadata is hidden from GUI by default.

Available columns:

| Column       | Description                         |
| ------------ | ----------------------------------- |
| COMMAND      | The command                         |
| EXIT_CODE    | Exit code of the command            |
| EXECUTED_AT  | Execution timestamp of the command  |
| EXECUTED_IN  | Execution duration of the command   |
| TMUX_SESSION | Tmux session context of the command |
| PATH         | Path context of the command         |

## Theme Attributes

The theme can be customized by changing attributes listed below.

| Attribute  | Description                      |
| ---------- | -------------------------------- |
| primary    | Primary foreground               |
| secondary  | Secondary foreground             |
| accent     | Accent color                     |
| background | Background of various components |
| border     | Border color of the components   |
