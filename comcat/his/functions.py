"""Common functions."""

from his import ACCOUNT, CUSTOMER

from comcatlib import User
from comcatlib.messages import NO_SUCH_USER


__all__ = ['get_user', 'get_users']


def get_user(ident):
    """Returns the respective ComCat user of the current customer."""

    if ACCOUNT.root:
        try:
            return User[ident]
        except User.DoesNotExist:
            raise NO_SUCH_USER

    try:
        return User.get((User.id == ident) & (User.customer == CUSTOMER.id))
    except User.DoesNotExist:
        raise NO_SUCH_USER


def get_users():
    """Yields ComCat users of the current customer."""

    if ACCOUNT.root:
        return User

    return User.select().where(User.customer == CUSTOMER.id)
