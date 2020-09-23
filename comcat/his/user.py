"""Management of ComCat users."""

from functools import wraps

from flask import request

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from comcatlib import User, Presentation
from comcatlib.messages import USER_ADDED
from comcatlib.messages import USER_DELETED
from comcatlib.messages import USER_PATCHED
from his import CUSTOMER, authenticated, authorized, root
from wsgilib import JSON, XML

from comcat.his.functions import get_user, get_users


__all__ = ['ROUTES']


def with_user(function):
    """Decorator to run the respective function
    with a user as first argument.
    """

    @wraps(function)
    def wrapper(ident, *args, **kwargs):
        """Wraps the original function."""
        return function(get_user(ident), *args, **kwargs)

    return wrapper


@authenticated
@authorized('comcat')
def list_():
    """Lists ComCat users."""

    return JSON([user.to_json(cascade=True) for user in get_users()])


@authenticated
@authorized('comcat')
@with_user
def get(user):
    """Returns the respective ComCat user."""

    return JSON(user.to_json(cascade=True))


@authenticated
@authorized('comcat')
@root
def add():
    """Adds a new ComCat user."""

    user = User.from_json(request.json, CUSTOMER.id, skip={'uuid'})
    user.save()
    return USER_ADDED.update(id=user.id, uuid=user.uuid.hex)


@authenticated
@authorized('comcat')
@root
@with_user
def patch(user):
    """Updates the respective user."""

    user.patch_json(request.json)
    user.save()
    return USER_PATCHED


@authenticated
@authorized('comcat')
@root
@with_user
def delete(user):
    """Deletes the respective user."""

    user.delete_instance()
    return USER_DELETED


@authenticated
@authorized('comcat')
@with_user
def get_presentation(user):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(user)

    try:
        request.args['xml']
    except KeyError:
        try:
            return JSON(presentation.to_json())
        except AmbiguousConfigurationsError:
            return AMBIGUOUS_CONFIGURATIONS
        except NoConfigurationFound:
            return NO_CONFIGURATION_ASSIGNED

    try:
        presentation_dom = presentation.to_dom()
    except AmbiguousConfigurationsError:
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


ROUTES = (
    ('GET', '/user', list_),
    ('GET', '/user/<int:ident>', get),
    ('POST', '/user', add),
    ('PATCH', '/user/<int:ident>', patch),
    ('DELETE', '/user/<int:ident>', delete),
    ('GET', '/user/<int:ident>/presentation', get_presentation)
)
