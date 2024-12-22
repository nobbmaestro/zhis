import os
from contextlib import contextmanager
from typing import Iterable, Optional, Type

from peewee import Model, SqliteDatabase

from zhis.db import History, Path, TmuxSession

db = SqliteDatabase(os.path.expanduser("~/.zsh_history.db"))

DATABASE_MODELS = (
    History,
    Path,
    TmuxSession,
)


@contextmanager
def database_connection(models: Optional[Iterable[Type[Model]]] = None):
    models = models or DATABASE_MODELS

    try:
        if db.is_closed():
            db.connect()
        db.bind(models)
        db.create_tables(models)

        yield

    finally:
        if not db.is_closed():
            db.close()
