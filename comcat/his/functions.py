"""Common functions."""

from his import CUSTOMER

from comcatlib import Account
from comcatlib.messages import NO_SUCH_ACCOUNT


__all__ = ['get_account', 'get_accounts']


def get_account(ident):
    """Returns the respective ComCat account of the current customer."""

    try:
        return Account.get(
            (Account.id == ident) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT


def get_accounts():
    """Yields ComCat accounts of the current customer."""

    return Account.select().where(Account.customer == CUSTOMER.id)
