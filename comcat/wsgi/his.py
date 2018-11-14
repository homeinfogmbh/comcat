"""HIS interface for account management."""

from his.messages.data import InvalidData, MissingData
from wsgilib import JSON

from comcat.orm import Account


def get_account(uuid):
    """Returns the respective account."""

    try:
        uuid = UUID(uuid)
    except ValueError:
        raise InvalidData(hint='Not a UUID.')
    except TypeError:
        raise MissingData(hint='No UUID specified.')

    try:
        return Account.get(
            (Account.uuid = uuid)
            & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NoSuchAccount()


def list_():
    """Lists accounts."""

    if ACCOUNT.root:
        accounts = Account
    else:
        accounts = Account.select().where(Account.customer == CUSTOMER.id)

    return JSON([account.to_json(skip=None) for account in accounts])


def get(uuid):
    """Returns the respective account."""

    account = get_account(uuid)
    return JSON(account.to_json(skip=None))
