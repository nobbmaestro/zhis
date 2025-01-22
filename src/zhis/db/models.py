# pytype: skip-file

import datetime
import logging
import re
from typing import Optional, Sequence

from peewee import (
    CharField,
    DatabaseProxy,
    DateTimeField,
    DoesNotExist,
    Field,
    ForeignKeyField,
    IntegerField,
    Model,
    ModelSelect,
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


class TmuxSession(BaseModel):
    session = CharField(unique=True)


class Path(BaseModel):
    path = CharField(unique=True)


class History(BaseModel):
    command = CharField()
    exit_code = IntegerField(null=True)
    executed_at = DateTimeField(default=datetime.datetime.now)
    executed_in = IntegerField(null=True)
    path_context = ForeignKeyField(Path, backref="histories", null=True)
    session_context = ForeignKeyField(TmuxSession, backref="histories", null=True)

    @classmethod
    def register_command(
        cls,
        command: str,
        tmux_session_context: Optional[str] = None,
        path_context: Optional[str] = None,
        exit_code: Optional[int] = None,
        executed_at: Optional[datetime.datetime] = None,
        executed_in: Optional[int] = None,
        exclude_commands: Optional[Sequence[str]] = None,
    ) -> int:
        exclude_commands = exclude_commands or []
        if any(re.search(pattern, command) for pattern in exclude_commands):
            logging.info("Command disallowed: %s", command)
            return -1

        executed_at = executed_at or datetime.datetime.now()

        tmux_session = TmuxSession.get_instance(
            TmuxSession.session, tmux_session_context
        )
        path = Path.get_instance(Path.path, path_context)

        logging.info(
            "Register command: %s, exit_code: %s, path: %s, tmux_session: %s",
            command,
            exit_code,
            path,
            tmux_session_context,
        )

        return cls.create(
            command=command,
            exit_code=exit_code,
            executed_at=executed_at,
            executed_in=executed_in,
            path_context=path,
            session_context=tmux_session,
        )

    @classmethod
    def edit_command(
        cls,
        command_id: int,
        executed_at: Optional[datetime.datetime] = None,
        executed_in: Optional[int] = None,
        exit_code: Optional[int] = None,
        path_context: Optional[str] = None,
        tmux_session_context: Optional[str] = None,
    ):
        try:
            cls.get_by_id(command_id)
        except DoesNotExist:
            logging.info("id '%s' does not exist.", command_id)
            return

        kwargs = {
            "executed_at": executed_at,
            "executed_in": executed_in,
            "exit_code": exit_code,
            "path_context": Path.get_instance(Path.path, path_context),
            "session_context": TmuxSession.get_instance(
                TmuxSession.session, tmux_session_context
            ),
        }

        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        if kwargs:
            cls.set_by_id(command_id, kwargs)

    @classmethod
    def query_history(
        cls,
        pattern: str = "",
        tmux_session_context: Optional[str] = None,
        path_context: Optional[str] = None,
        exit_code: Optional[int] = None,
        limit: Optional[int] = None,
        base_query: Optional[ModelSelect] = None,
    ) -> ModelSelect:
        query = base_query or cls.select().order_by(cls.executed_at.desc())

        query = query.where(History.command.contains(pattern))

        if tmux_session_context is not None:
            tmux_session_id = TmuxSession.get_or_none(session=tmux_session_context)
            query = query.where(cls.session_context == tmux_session_id)

        if path_context is not None:
            path_id = Path.get_or_none(path=path_context)
            query = query.where(cls.path_context == path_id)

        if exit_code is not None:
            query = query.where(cls.exit_code == exit_code)

        if limit is not None:
            query = query.limit(limit)

        return query

    @classmethod
    def get_previous_command(
        cls,
        tmux_session_context: Optional[str] = None,
        path_context: Optional[str] = None,
        exit_code: Optional[int] = None,
    ) -> "History":
        return cls.query_history(
            tmux_session_context=tmux_session_context,
            path_context=path_context,
            exit_code=exit_code,
        ).first()  # type: ignore
