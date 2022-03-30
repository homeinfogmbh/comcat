"""Common functions."""

from functools import wraps
from typing import Annotated, Callable, Iterator

from peewee import ModelSelect

from cmslib import BaseChart, Group
from comcatlib import GroupMemberUser
from comcatlib import InvalidAddress
from comcatlib import MenuBaseChart
from comcatlib import User
from comcatlib import UserDamageReport
from comcatlib import UserRegistration
from his import CUSTOMER
from mdb import Address, Customer, Tenement

from comcat.his.grouptree import GroupTree


__all__ = [
    'get_address',
    'get_customer',
    'get_group_member_user',
    'get_group_member_users',
    'get_groups_tree',
    'get_menu_base_chart',
    'get_menu_base_charts',
    'get_tenement',
    'get_tenements',
    'get_user',
    'get_users',
    'get_user_registration',
    'get_user_registrations',
    'get_user_damage_reports',
    'get_user_damage_report',
    'with_user'
]


def get_address(address: Annotated[list[str], 4]) -> Address:
    """Returns the specified address.

    Do NOT allow getting addresses by ID to mitigate sniffing!
    """

    try:
        address = Address.add(*address)
    except (TypeError, ValueError):
        raise InvalidAddress() from None

    if not address.id:
        address.save()

    return address


def get_customer(ident: int) -> Customer:
    """Returns the specified customer."""

    return Customer.select(cascade=True).where(Customer.id == ident).get()


def get_group_member_user(ident: int) -> GroupMemberUser:
    """Returns the requested group <-> user mapping."""

    return get_group_member_users().where(GroupMemberUser.id == ident).get()


def get_group_member_users() -> ModelSelect:
    """Selects group <-> user mappings."""

    return GroupMemberUser.select(cascade=True).where(
        Tenement.customer == CUSTOMER.id
    )


def get_groups_tree() -> Iterator[GroupTree]:
    """Returns the management tree."""

    for root_group in Group.select(cascade=True).where(
            (Group.customer == CUSTOMER.id) & (Group.parent >> None)
    ):
        yield GroupTree(root_group)


def get_menu_base_chart(ident: int) -> MenuBaseChart:
    """Returns the respective base chart menu."""

    return get_menu_base_charts().where(MenuBaseChart.id == ident).get()


def get_menu_base_charts() -> ModelSelect:
    """Yields base chart menus for the given base chart."""

    return MenuBaseChart.select(cascade=True).where(
        BaseChart.customer == CUSTOMER.id
    )


def get_tenement(ident: int) -> Tenement:
    """Returns the given tenement by ID for the current customer."""

    return get_tenements().where(Tenement.id == ident).get()


def get_tenements() -> ModelSelect:
    """Yields tenements of the current user."""

    return Tenement.select(cascade=True).where(
        Tenement.customer == CUSTOMER.id
    )


def get_user(ident: int) -> User:
    """Returns the respective ComCat user of the current customer."""

    return get_users().where(User.id == ident).get()


def get_users() -> ModelSelect:
    """Yields ComCat users of the current customer."""

    return User.select(cascade=True).where(Tenement.customer == CUSTOMER.id)


def get_user_registration(ident: int) -> UserRegistration:
    """Returns the selected user registration."""

    return get_user_registrations().where(UserRegistration.id == ident).get()


def get_user_registrations() -> ModelSelect:
    """Selects user registrations of the current customer."""

    return UserRegistration.select(cascade=True).where(
        UserRegistration.customer == CUSTOMER.id
    )


def get_user_damage_report(ident: int) -> UserDamageReport:
    """Returns a damage report with the given ID."""

    return get_user_damage_reports().where(
        UserDamageReport.id == ident
    ).get()


def get_user_damage_reports() -> ModelSelect:
    """Yields damage reports for the current user."""

    return UserDamageReport.select().join(User).join(Tenement).where(
        Tenement.customer == CUSTOMER.id
    )


def with_user(function: Callable) -> Callable:
    """Decorator to run the respective function
    with a user as first argument.
    """

    @wraps(function)
    def wrapper(ident: int, *args, **kwargs):
        """Wraps the original function."""
        return function(get_user(ident), *args, **kwargs)

    return wrapper
