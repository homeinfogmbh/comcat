"""Object-relational mappings."""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import BooleanField
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
    expires = DateTimeField(null=True)
    locked = BooleanField(default=False)

    @classmethod
    def add(cls, customer, passwd=None):
        """Creates a new account."""
        account = cls()
        account.customer = customer
        account.passwd = passwd
        account.save()
        return account

    @property
    def valid(self):
        """Determines whether the account may be used."""
        if self.locked:
            return False

        return self.expires is None or self.expires > datetime.now()


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


class Session(_ComCatModel):
    """A ComCat session."""

    uuid = UUIDField()
    account = ForeignKeyField(
        Account, column_name='account', backref='sessions',
        on_delete='CASCADE')
    start = DateTimeField(default=datetime.now)
    end = DateTimeField()

    @classmethod
    def open(cls, account, duration=timedelta(minutes=15)):
        """Opens a new session for the respective account."""
        now = datetime.now()
        session = cls(account=account, start=now, end=now+duration)
        session.save()
        return session

    @property
    def exists(self):
        """Determines whether the session still exists in the database."""
        try:
            return type(self)[self.id]
        except self.DoesNotExist:
            return False

    @property
    def active(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() <= self.end

    @property
    def valid(self):
        """Determines whether the session is valid."""
        return self.active and self.exists and self.account.valid
