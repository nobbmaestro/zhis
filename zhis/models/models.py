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


class CliCommand(BaseModel):
    command = CharField(unique=True)


class TmuxSession(BaseModel):
    session = CharField(unique=True)


class Path(BaseModel):
    path = CharField(unique=True)


class History(BaseModel):
    command = ForeignKeyField(CliCommand, backref="histories")
    exit_code = IntegerField(null=True)
    last_execution = DateTimeField(default=datetime.datetime.now)
    session = ForeignKeyField(TmuxSession, backref="histories")
    path = ForeignKeyField(Path, backref="histories")
