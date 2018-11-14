"""Object-relational mappings."""

from uuid import uuid4

from peewee import CharField, ForeignKeyField, UUIDField

from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from comcat.config import CONFIG


__all__ = ['Account']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _ComCatModel(JSONModel):
    """Basic comcat model."""

    class Meta:     # pylint: disable=C0111
        database = DATABASE
        schema = database.schema


class Account(_ComCatModel):
    """A ComCat account."""

    uuid = UUIDField(default=uuid4)
    customer = ForeignKeyField(Customer, column_name='customer')
    rental_unit = CharField(255, null=True)

    def to_json(self, *args, unsafe=False, skip=(), **kwargs):
        """Converts the account to JSON,
        suppressing the UUID per default.
        """
        if not unsafe:
            skip = (tuple(skip) if skip else ()) + ('uuid',)

        return super().to_json(*args, skip=skip, **kwargs)
