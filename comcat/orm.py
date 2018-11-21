"""Object-relational mappings."""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import UUIDField

from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, Argon2Field

from comcat.config import CONFIG
from comcat.crypto import genpw


__all__ = ['Account']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _ComCatModel(JSONModel):
    """Basic comcat model."""

    class Meta:     # pylint: disable=C0111
        database = DATABASE
        schema = database.database


class Account(_ComCatModel):
    """A ComCat account."""

    uuid = UUIDField(default=uuid4)
    passwd = Argon2Field(null=True)
    customer = ForeignKeyField(Customer, column_name='customer')
    annotation = CharField(255)
    created = DateTimeField(default=datetime.now)
    last_login = DateTimeField(null=True)

    @classmethod
    def add(cls, customer, passwd=None):
        """Creates a new account."""
        account = cls()
        account.customer = customer
        account.passwd = passwd
        account.save()
        return account


class FirstLoginToken(_ComCatModel):
    """Tokens for first login creation."""

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')
    uuid = UUIDField(default=uuid4)
    valid_from = DateTimeField()
    valid_until = DateTimeField()

    @classmethod
    def add(cls, account):
        """Creates a new first """
        now = datetime.now()
        expires = now + timedelta(days=14)
        token = cls(account=account, valid_from=now, valid_until=expires)
        token.save()
        return token

    def init_account(self):
        """Initializes the respective account with a random password."""
        passwd = genpw()
        self.account.passwd = passwd
        self.account.save()
        self.delete_instance()
        return passwd
