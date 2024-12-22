import datetime

from peewee import (
    CharField,
    DatabaseProxy,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
)

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


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
