"""Management of ComCat users."""

from functools import wraps
from typing import Callable, Union

from flask import request

from his import authenticated, authorized, root
from wsgilib import JSON, JSONMessage, XML

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS

from comcatlib import DuplicateUser, User, Presentation
from comcatlib.functions import genpw
from comcatlib.messages import DUPLICATE_USER
from comcatlib.messages import USER_ADDED
from comcatlib.messages import USER_DELETED
from comcatlib.messages import USER_PATCHED

from comcat.his.functions import get_tenement, get_user, get_users


__all__ = ['ROUTES']


def with_user(function: Callable) -> Callable:
    """Decorator to run the respective function
    with a user as first argument.
    """

    @wraps(function)
    def wrapper(user: int, *args, **kwargs):
        """Wraps the original function."""
        return function(get_user(user), *args, **kwargs)

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
    return USER_PATCHED.update(passwd=passwd)


@authenticated
@authorized('comcat')
@root
def add() -> JSONMessage:
    """Adds a new ComCat user."""

    tenement = get_tenement(request.json.pop('tenement'))

    try:
        user, passwd = User.from_json(request.json, tenement, skip={'uuid'})
    except DuplicateUser:
        return DUPLICATE_USER

    user.save()
    return USER_ADDED.update(id=user.id, passwd=passwd)


@authenticated
@authorized('comcat')
@root
@with_user
def patch(user: User) -> JSONMessage:
    """Updates the respective user."""

    user.patch_json(request.json)
    user.save()
    return USER_PATCHED


@authenticated
@authorized('comcat')
@root
@with_user
def delete(user: User) -> JSONMessage:
    """Deletes the respective user."""

    user.delete_instance()
    return USER_DELETED


@authenticated
@authorized('comcat')
@with_user
def get_presentation(user: User) -> Union[JSON, JSONMessage, XML]:
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(user)

    try:
        if 'xml' in request.args:
            return XML(presentation.to_dom())

        return JSON(presentation.to_json())
    except AmbiguousConfigurationsError:
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED


ROUTES = (
    ('GET', '/user', list_),
    ('GET', '/user/<int:ident>', get),
    ('PUT', '/user/<int:ident>/pwgen', resetpw),
    ('POST', '/user', add),
    ('PATCH', '/user/<int:ident>', patch),
    ('DELETE', '/user/<int:ident>', delete),
    ('GET', '/user/<int:ident>/presentation', get_presentation)
)
