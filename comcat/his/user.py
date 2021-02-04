"""Management of ComCat users."""

from functools import wraps
from typing import Callable, Union

from flask import request

from his import authenticated, authorized, root
from wsgilib import JSON, JSONMessage, XML

from comcatlib import User, Presentation
from comcatlib.functions import genpw

from comcat.his.functions import get_tenement, get_user, get_users


__all__ = ['ROUTES']


def with_user(function: Callable) -> Callable:
    """Decorator to run the respective function
    with a user as first argument.
    """

    @wraps(function)
    def wrapper(ident: int, *args, **kwargs):
        """Wraps the original function."""
        return function(get_user(ident), *args, **kwargs)

    return wrapper


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists ComCat users."""

    return JSON([user.to_json(cascade=True) for user in get_users()])


@authenticated
@authorized('comcat')
@with_user
def get(user: User) -> JSON:
    """Returns the respective ComCat user."""

    return JSON(user.to_json(cascade=True))


@authenticated
@authorized('comcat')
@with_user
def resetpw(user: User) -> JSONMessage:
    """Generates a new, random password for the respective user."""

    user.passwd = passwd = genpw()
    user.save()
    return JSONMessage('Password reset.', passwd=passwd, status=200)


@authenticated
@authorized('comcat')
@root
def add() -> JSONMessage:
    """Adds a new ComCat user."""

    tenement = get_tenement(request.json.pop('tenement'))
    user, passwd = User.from_json(request.json, tenement)
    user.save()
    return JSONMessage('User added.', id=user.id, passwd=passwd, status=201)


@authenticated
@authorized('comcat')
@root
@with_user
def patch(user: User) -> JSONMessage:
    """Updates the respective user."""

    tenement = request.json.pop('tenement', None)

    if tenement is not None:
        tenement = get_tenement(tenement)

    user.patch_json(request.json, tenement)
    user.save()
    return JSONMessage('User patched.', status=200)


@authenticated
@authorized('comcat')
@root
@with_user
def delete(user: User) -> JSONMessage:
    """Deletes the respective user."""

    user.delete_instance()
    return JSONMessage('User deleted.', status=200)


@authenticated
@authorized('comcat')
@with_user
def get_presentation(user: User) -> Union[JSON, JSONMessage, XML]:
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(user)

    if 'xml' in request.args:
        return XML(presentation.to_dom())

    return JSON(presentation.to_json())


ROUTES = (
    ('GET', '/user', list_),
    ('GET', '/user/<int:ident>', get),
    ('GET', '/user/<int:ident>/pwgen', resetpw),
    ('POST', '/user', add),
    ('PATCH', '/user/<int:ident>', patch),
    ('DELETE', '/user/<int:ident>', delete),
    ('GET', '/user/<int:ident>/presentation', get_presentation)
)
