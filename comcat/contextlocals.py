"""Context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from comcatlib.messages import AccountSubsitutionUnauthorized
from comcatlib.messages import CustomerSubsitutionUnauthorized
from comcatlib.messages import NoSessionTokenSpecified
from comcatlib.messages import NoSuchAccount
from comcatlib.messages import NoSuchCustomer
from comcatlib.messages import NoSuchSession
from comcatlib.orm import Account, Session


__all__ = ['ACCOUNT', 'CUSTOMER', 'SESSION']


def get_session():
    """Returns the current session."""

    try:
        token = request.headers['ComCat-Session']
    except KeyError:
        raise NoSessionTokenSpecified()

    try:
        token = UUID(token)
    except ValueError:
        raise NoSuchSession()   # Mitigate sniffing.

    try:
        return Session.get(Session.token == token)
    except Session.DoesNotExist:
        raise NoSuchSession()


def get_account():
    """Returns the currently used account."""

    try:
        uuid = request.headers['ComCat-Account']
    except KeyError:
        return SESSION.account

    if not SESSION.account.root:
        raise AccountSubsitutionUnauthorized()

    try:
        uuid = UUID(uuid)
    except ValueError:
        raise NoSuchAccount()   # Mitigate sniffing.

    try:
        return Account.get(Account.uuid == uuid)
    except Account.DoesNotExist:
        raise NoSuchAccount()


def get_customer():
    """Returns the currently used customer."""

    try:
        cid = request.headers['ComCat-Customer']
    except KeyError:
        return ACCOUNT.customer

    if not ACCOUNT.root:
        raise CustomerSubsitutionUnauthorized()

    try:
        cid = int(cid)
    except ValueError:
        raise NoSuchCustomer()   # Mitigate sniffing.

    try:
        return Customer.get(Customer.id == cid)
    except Account.DoesNotExist:
        raise NoSuchCustomer()


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(get_account)
CUSTOMER = LocalProxy(get_customer)
