import datetime
import logging
import re
from typing import Optional, Sequence

from peewee import (
    CharField,
    DatabaseProxy,
    DateTimeField,
    Field,
    ForeignKeyField,
    IntegerField,
    Model,
)

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy

    @classmethod
    def get_instance(
        cls,
        field: Field,
        value: Optional[str] = None,
    ):
        return cls.get_or_create(**{field.name: value})[0] if value else None


class CliCommand(BaseModel):
    command = CharField(unique=True)


class TmuxSession(BaseModel):
    session = CharField(unique=True)


class Path(BaseModel):
    path = CharField(unique=True)


class History(BaseModel):
    command = ForeignKeyField(CliCommand, backref="histories")
    exit_code = IntegerField(null=True)
    executed_at = DateTimeField(default=datetime.datetime.now)
    path_context = ForeignKeyField(Path, backref="histories", null=True)
    session_context = ForeignKeyField(TmuxSession, backref="histories", null=True)

    @classmethod
    def register_command(
        cls,
        command: str,
        session_context: Optional[str] = None,
        path_context: Optional[str] = None,
        exit_code: Optional[int] = None,
        executed_at: Optional[datetime.datetime] = None,
        exclude_commands: Optional[Sequence[str]] = None,
    ):
        exclude_commands = exclude_commands or []
        if any(re.match(pattern, command) for pattern in exclude_commands):
            logging.info("Command disallowed: %s", command)
            return

        executed_at = executed_at or datetime.datetime.now()

        cli_command_instance = CliCommand.get_instance(CliCommand.command, command)
        tmux_session = TmuxSession.get_instance(TmuxSession.session, session_context)
        path = Path.get_instance(Path.path, path_context)

        logging.info(
            "Register command: %s, exit_code: %s, path: %s, tmux_session: %s",
            command,
            exit_code,
            path,
            session_context,
        )

        cls.create(
            command=cli_command_instance,
            exit_code=exit_code,
            executed_at=executed_at,
            path_context=path,
            session_context=tmux_session,
        )

    @classmethod
    def get_previous_command(
        cls,
        tmux_session_context: str = "",
    ) -> "History":
        query = cls.select().order_by(History.executed_at.desc())

        if tmux_session_context:
            tmux_session_id = TmuxSession.get_or_none(session=tmux_session_context)
            query = query.where(cls.session_context == tmux_session_id)

        return query.first()

    @classmethod
    def query_history(
        cls,
        pattern: str = "",
        tmux_session_context: str = "",
    ) -> Sequence["History"]:
        query = cls.select().order_by(cls.executed_at.desc())

        if pattern:
            query = query.join(CliCommand).where(CliCommand.command ** f"%{pattern}%")

        if tmux_session_context:
            tmux_session_id = TmuxSession.get_or_none(session=tmux_session_context)
            query = query.where(cls.session_context == tmux_session_id)

        return list(query)
