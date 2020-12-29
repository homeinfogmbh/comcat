"""Management of menus assigned to ComCat accounts."""

from typing import Iterable

from flask import request

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import NO_SUCH_CONTENT
from comcatlib import User, UserMenu
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


def list_user_menus(user: int) -> Iterable[UserMenu]:
    """Lists menus assignments for the given user."""

    return UserMenu.select().join(User).where(
        (User.id == user) & (User.customer == CUSTOMER))


def get_user_menu(ident: int) -> Iterable:
    """Returns the respective UserMenu for the current customer context."""

    return UserMenu.select().join(User).where(
        (UserMenu.id == ident) & (User.customer == CUSTOMER)
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

    user_menu = UserMenu.from_json(request.json)
    user_menu.save()
    return CONTENT_ADDED.update(id=user_menu.id)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes the menu from the respective account."""

    try:
        user_menu = get_user_menu(ident)
    except UserMenu.DoesNotExist:
        raise NO_SUCH_CONTENT from None

    user_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/user/menu/<int:ident>', get),
    ('GET', '/content/user/<int:user>/menu', list_),
    ('POST', '/content/user/menu', add),
    ('DELETE', '/content/user/menu/<int:ident>', delete)
)
