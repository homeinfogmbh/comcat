"""Object-relational mappings."""

from datetime import datetime, timedelta
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import UUIDField

from his.messages import AccountLocked, DurationOutOfBounds, InvalidCredentials
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, Argon2Field

from comcat.config import CONFIG
from comcat.exceptions import InvalidInitializationToken, InvalidSession


__all__ = ['Account']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])
ALLOWED_SESSION_DURATIONS = range(5, 31)
DEFAULT_SESSION_DURATION = 15
MAX_FAILED_LOGINS = 5


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
    failed_logins = IntegerField(default=0)
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

    @property
    def can_login(self):
        """Determines whether the account may login."""
        return self.valid and self.failed_logins <= MAX_FAILED_LOGINS

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

    def login(self, passwd):
        """Performs a login."""
        if self.can_login:
            try:
                self.passwd.verify(passwd)
            except VerifyMismatchError:
                self.failed_logins += 1
                self.save()
                raise InvalidCredentials()

            if self.passwd.needs_rehash:
                self.passwd = passwd

            self.failed_logins = 0
            self.last_login = datetime.now()
            self.save()
            return True

        raise AccountLocked()


class InitializationToken(_ComCatModel):
    """Tokens for first login creation."""

    class Meta:     # pylint: disable=C0111
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
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DurationOutOfBounds()

        now = datetime.now()
        duration = timedelta(minutes=duration)
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
