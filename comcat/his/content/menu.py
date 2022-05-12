"""Management of menus assigned to ComCat accounts."""

from typing import Iterable

from flask import request

from comcatlib import User, UserMenu
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage

from comcat.his.functions import get_user, get_menu


__all__ = ['ROUTES']


def list_user_menus(user: int) -> Iterable[UserMenu]:
    """Lists menus assignments for the given user."""

    return UserMenu.select(cascade=True).where(
        (User.id == user) & (User.customer == CUSTOMER.id))


def get_user_menu(ident: int) -> UserMenu:
    """Returns the respective UserMenu for the current customer context."""

    return UserMenu.select(cascade=True).where(
        (UserMenu.id == ident) & (User.customer == CUSTOMER.id)
    ).get()


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Returns the respective UserMenu."""

    return JSON(get_user_menu(ident).to_json())


@authenticated
@authorized('comcat')
def list_(user: int) -> JSON:
    """Returns a list of user menus in the respective account."""

    return JSON([user_menu.to_json() for user_menu in list_user_menus(user)])


@authenticated
@authorized('comcat')
def add() -> JSONMessage:
    """Adds the menu to the respective account."""

    user_menu = UserMenu.from_json(
        request.json,
        get_user(request.json.pop('user')),
        get_menu(request.json.pop('menu'), CUSTOMER.id)
    )
    user_menu.save()
    return JSONMessage('User menu added.', id=user_menu.id, status=201)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes the menu from the respective account."""

    user_menu = get_user_menu(ident)
    user_menu.delete_instance()
    return JSONMessage('User menu deleted.', status=200)


ROUTES = (
    ('GET', '/content/user/menu/<int:ident>', get),
    ('GET', '/content/user/<int:user>/menu', list_),
    ('POST', '/content/user/menu', add),
    ('DELETE', '/content/user/menu/<int:ident>', delete)
)
