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
from comcat.exceptions import InvalidInitializationToken, InvalidSession


__all__ = ['Account']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])
DEFAULT_SESSION_DURATION = timedelta(minutes=15)


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

    def initialize(self, token, passwd):
        """Initializes the respective account with a random password."""
        try:
            token = self.initialization_tokens.where(
                InitializationToken.token == token).get()
        except InitializationToken.DoesNotExist:
            raise InvalidInitializationToken()

        if not token.valid:
            raise InvalidInitializationToken()

        self.passwd = passwd
        token.delete_instance()
        return self.save()


class InitializationToken(_ComCatModel):
    """Tokens for first login creation."""

    class Meta:
        table_name = 'initialization_token'

    account = ForeignKeyField(
        Account, column_name='account', backref='initialization_tokens',
        on_delete='CASCADE')
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

    @property
    def valid(self):
        """Determines whether the login token is valid."""
        return self.valid_from <= datetime.now() <= self.valid_until


class Session(_ComCatModel):
    """A ComCat session."""

    token = UUIDField(default=uuid4)
    account = ForeignKeyField(
        Account, column_name='account', backref='sessions',
        on_delete='CASCADE')
    start = DateTimeField(default=datetime.now)
    end = DateTimeField()

    @classmethod
    def open(cls, account, duration=DEFAULT_SESSION_DURATION):
        """Opens a new session for the respective account."""
        now = datetime.now()
        session = cls(account=account, start=now, end=now+duration)
        session.save()
        return session

    @classmethod
    def fetch(cls, token):
        """Returns the respective session."""
        try:
            session = cls.get(cls.token == token)
        except cls.DoesNotExist:
            raise InvalidSession()

        if session.valid:
            return session

        raise InvalidSession()

    @property
    def active(self):
        """Determines whether the session is active."""
        return self.start <= datetime.now() <= self.end

    @property
    def valid(self):
        """Determines whether the session is valid."""
        return self.active and self.account.valid
