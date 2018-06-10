from peewee import *

db = SqliteDatabase('user_info.db')


class User(Model):
    name = CharField()
    sex = IntField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db  # This model uses the "user_info.db" database.
