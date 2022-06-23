"""User registration management."""

from flask import request

from comcatlib import DuplicateUser, notify_user
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json

from comcat.his.functions import get_tenement
from comcat.his.functions import get_user_registrations
from comcat.his.functions import get_user_registration


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists user registrations."""

    return JSON([ur.to_json() for ur in get_user_registrations(CUSTOMER.id)])


@authenticated
@authorized('comcat')
@require_json(dict)
def accept(ident: int) -> JSONMessage:
    """Accept a registration."""

    user_registration = get_user_registration(ident, CUSTOMER.id)
    tenement = get_tenement(request.json.get('tenement'), CUSTOMER.id)

    try:
        user, passwd = user_registration.confirm(tenement)
    except DuplicateUser:
        return JSONMessage('User already exists.', status=400)

    user.save()
    notify_user(user.email, passwd)
    return JSONMessage('Added user.', id=user.id, status=201)


@authenticated
@authorized('comcat')
def deny(ident: int) -> JSONMessage:
    """Deny a registration."""

    user_registration = get_user_registration(ident, CUSTOMER.id)
    user_registration.delete_instance()
    return JSONMessage('User registration denied.', status=200)


ROUTES = [
    ('GET', '/registration', list_),
    ('POST', '/registration/<int:ident>', accept),
    ('DELETE', '/registration/<int:ident>', deny)
]
