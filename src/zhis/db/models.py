# pytype: skip-file

import datetime
import logging
from typing import Optional

from peewee import (
    CharField,
    DatabaseProxy,
    DateTimeField,
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
    ):
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

        cls.create(
            command=command,
            exit_code=exit_code,
            executed_at=executed_at,
            path_context=path,
            session_context=tmux_session,
        )

    @classmethod
    def query_history(
        cls,
        pattern: str = "",
        tmux_session_context: Optional[str] = None,
        path_context: Optional[str] = None,
        exit_code: Optional[int] = None,
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
