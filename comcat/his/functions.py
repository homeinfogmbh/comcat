"""Common functions."""

from typing import Iterable

from his import ACCOUNT, CUSTOMER
from mdb import Tenement

from comcatlib import User, UserDamageReport
from comcatlib.messages import NO_SUCH_DAMAGE_REPORT
from comcatlib.messages import NO_SUCH_TENEMENT
from comcatlib.messages import NO_SUCH_USER


__all__ = [
    'get_tenement',
    'get_tenements',
    'get_user',
    'get_users',
    'get_user_damage_reports',
    'get_user_damage_report'
]


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

    select = User.select().join(Tenement)

    if ACCOUNT.root:
        return select.where(True)

    return select.where(Tenement.customer == CUSTOMER.id)


def get_user_damage_reports() -> Iterable[UserDamageReport]:
    """Yields damage reports for the current user."""

    return UserDamageReport.select().join(User).join(Tenement).where(
        Tenement.customer == CUSTOMER.id)


def get_user_damage_report(ident: int) -> UserDamageReport:
    """Returns a damage report with the given ID."""

    try:
        return get_user_damage_reports().where(
            UserDamageReport.id == ident).get()
    except UserDamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT from None
