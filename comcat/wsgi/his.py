"""HIS interface for account management."""

from uuid import UUID

from his import ACCOUNT, CUSTOMER, authenticated, authorized
from his.messages.data import InvalidData, MissingData
from wsgilib import JSON

from comcat.messages import NoSuchAccount
from comcat.orm import Account


__all__ = ['ROUTES', 'get_account']


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
            (Account.uuid == uuid) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NoSuchAccount()


@authenticated
@authorized('comcat')
def list_():
    """Lists accounts."""

    if ACCOUNT.root:
        accounts = Account
    else:
        accounts = Account.select().where(Account.customer == CUSTOMER.id)

    return JSON([account.to_json(skip=None) for account in accounts])


@authenticated
@authorized('comcat')
def get(uuid):
    """Returns the respective account."""

    account = get_account(uuid)
    return JSON(account.to_json(skip=None))


ROUTES = (
    ('GET', '/', list_, 'list_accounts'),
    ('GET', '/<str:uuid>', get, 'get_account'))
