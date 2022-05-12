"""Common functions."""

from typing import Annotated, Iterator, Union

from peewee import ModelSelect

from cmslib import BaseChart, Configuration, Group, Menu
from comcatlib import GroupMemberUser
from comcatlib import InvalidAddress
from comcatlib import MenuBaseChart
from comcatlib import User
from comcatlib import UserDamageReport
from comcatlib import UserRegistration
from mdb import Address, Customer, Tenement

from comcat.his.grouptree import GroupTree


__all__ = [
    'get_address',
    'get_configuration',
    'get_configurations',
    'get_customer',
    'get_group_member_user',
    'get_group_member_users',
    'get_groups_tree',
    'get_menu',
    'get_menus',
    'get_menu_base_chart',
    'get_menu_base_charts',
    'get_tenement',
    'get_tenements',
    'get_user',
    'get_users',
    'get_user_registration',
    'get_user_registrations',
    'get_user_damage_reports',
    'get_user_damage_report'
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


def get_configuration(
        ident: int,
        customer: Union[Customer, int]
) -> Configuration:
    """Returns the selected configuration."""

    return get_configurations(customer).where(Configuration.id == ident).get()


def get_configurations(customer: Union[Customer, int]) -> ModelSelect:
    """Selects configurations of the given customer."""

    return Configuration.select().where(Configuration.customer == customer)


def get_customer(ident: int) -> Customer:
    """Returns the specified customer."""

    return Customer.select(cascade=True).where(Customer.id == ident).get()


def get_group_member_user(
        ident: int,
        customer: Union[Customer, int]
) -> GroupMemberUser:
    """Returns the requested group <-> user mapping."""

    return get_group_member_users(customer).where(
        GroupMemberUser.id == ident
    ).get()


def get_group_member_users(customer: Union[Customer, int]) -> ModelSelect:
    """Selects group <-> user mappings."""

    return GroupMemberUser.select(cascade=True).where(
        Tenement.customer == customer
    )


def get_groups_tree(customer: Union[Customer, int]) -> Iterator[GroupTree]:
    """Returns the management tree."""

    for root_group in Group.select(cascade=True).where(
            (Group.customer == customer) & (Group.parent >> None)
    ):
        yield GroupTree(root_group)


def get_menu(ident: int, customer: Union[Customer, int]) -> Menu:
    """Returns the selected menu."""

    return get_menus(customer).where(Menu.id == ident).get()


def get_menus(customer: Union[Customer, int]) -> ModelSelect:
    """Selects menus of the given customer."""

    return Menu.select().where(Menu.customer == customer)


def get_menu_base_chart(
        ident: int,
        customer: Union[Customer, int]
) -> MenuBaseChart:
    """Returns the respective base chart menu."""

    return get_menu_base_charts(customer).where(
        MenuBaseChart.id == ident
    ).get()


def get_menu_base_charts(customer: Union[Customer, int]) -> ModelSelect:
    """Yields base chart menus for the given base chart."""

    return MenuBaseChart.select(cascade=True).where(
        BaseChart.customer == customer
    )


def get_tenement(ident: int, customer: Union[Customer, int]) -> Tenement:
    """Returns the given tenement by ID for the current customer."""

    return get_tenements(customer).where(Tenement.id == ident).get()


def get_tenements(customer: Union[Customer, int]) -> ModelSelect:
    """Yields tenements of the current user."""

    return Tenement.select(cascade=True).where(
        Tenement.customer == customer
    )


def get_user(ident: int, customer: Union[Customer, int]) -> User:
    """Returns the respective ComCat user of the current customer."""

    return get_users(customer).where(User.id == ident).get()


def get_users(customer: Union[Customer, int]) -> ModelSelect:
    """Yields ComCat users of the current customer."""

    return User.select(cascade=True).where(Tenement.customer == customer)


def get_user_registration(
        ident: int,
        customer: Union[Customer, int]
) -> UserRegistration:
    """Returns the selected user registration."""

    return get_user_registrations(customer).where(
        UserRegistration.id == ident
    ).get()


def get_user_registrations(customer: Union[Customer, int]) -> ModelSelect:
    """Selects user registrations of the current customer."""

    return UserRegistration.select(cascade=True).where(
        UserRegistration.customer == customer
    )


def get_user_damage_report(
        ident: int,
        customer: Union[Customer, int]
) -> UserDamageReport:
    """Returns a damage report with the given ID."""

    return get_user_damage_reports(customer).where(
        UserDamageReport.id == ident
    ).get()


def get_user_damage_reports(customer: Union[Customer, int]) -> ModelSelect:
    """Yields damage reports for the current user."""

    return UserDamageReport.select().join(User).join(Tenement).where(
        Tenement.customer == customer
    )
