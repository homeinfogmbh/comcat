"""Management of ComCat users."""

from typing import Union

from flask import request

from his import CUSTOMER, admin, authenticated, authorized
from wsgilib import JSON, JSONMessage, XML

from comcatlib import Presentation, User

from comcat.functions import logout
from comcat.his.functions import get_tenement, get_users, with_user


__all__ = ['ROUTES']


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
@admin
@with_user
def patch(user: User) -> JSONMessage:
    """Updates the respective user."""

    tenement = request.json.pop('tenement', None)

    if tenement is not None:
        tenement = get_tenement(tenement, CUSTOMER.id)

    try:
        user.patch_json(
            request.json, tenement=tenement, skip={'created', 'passwd'}
        )
    except ValueError as error:
        return JSONMessage('Invalid data.', details=str(error), status=400)

    user.save()
    return JSONMessage('User patched.', status=200)


@authenticated
@authorized('comcat')
@admin
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


@authenticated
@authorized('comcat')
@with_user
def logout_(user: User) -> JSONMessage:
    """Deletes the respective user."""

    logout(user)
    return JSONMessage('User logged out.', status=200)


ROUTES = [
    ('GET', '/user', list_),
    ('GET', '/user/<int:ident>', get),
    ('PATCH', '/user/<int:ident>', patch),
    ('DELETE', '/user/<int:ident>', delete),
    ('GET', '/user/<int:ident>/presentation', get_presentation),
    ('DELETE', '/user/<int:ident>/logout', logout_)
]
