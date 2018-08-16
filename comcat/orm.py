"""Object relational mappings."""

from uuid import uuid4

from peewee import UUIDField

from peeweeplus import MySQLDatabase, JSONModel, Argon2Field


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _ComCatModel(JSONModel):
    """Basic comcat model."""

    class Meta:
        database = DATABASE
        schema = database.schema


class ComCatAccount(_ComCatModel):
    """A ComCat account."""

    uuid = UUIDField(default=uuid4)
    passwd = Argon2Field()
    customer = ForeignKeyField(Customer)
    address = ForeignKeyField(Address)
