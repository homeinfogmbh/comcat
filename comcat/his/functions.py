"""Common functions."""

from typing import Iterable

from his import ACCOUNT, CUSTOMER
from mdb import Tenement

from comcatlib import User
from comcatlib.messages import NO_SUCH_TENEMENT, NO_SUCH_USER


__all__ = ['get_tenement', 'get_tenements', 'get_user', 'get_users']


def get_tenement(ident: int) -> Tenement:
    """Returns the given tenement by ID for the current customer."""

    try:
        return get_tenements().where(Tenement.id == ident).get()
    except Tenement.DoesNotExist:
        raise NO_SUCH_TENEMENT from None


def get_tenements() -> Iterable[Tenement]:
    """Yields tenements of the current user."""

    if ACCOUNT.root:
        return Tenement.select().where(True)

    return Tenement.select().where(Tenement.customer == CUSTOMER.id)


def get_user(ident: int) -> User:
    """Returns the respective ComCat user of the current customer."""

    try:
        return get_users().where(User.id == ident).get()
    except User.DoesNotExist:
        raise NO_SUCH_USER from None


def get_users() -> Iterable[User]:
    """Yields ComCat users of the current customer."""

    if ACCOUNT.root:
        return User.select().where(True)

    return User.select().where(User.customer == CUSTOMER.id)
