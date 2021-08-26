"""User registration management."""

from flask import request

from wsgilib import JSON, JSONMessage, require_json

from comcat.his.functions import get_tenement
from comcat.his.functions import get_user_registrations
from comcat.his.functions import get_user_registration


__all__ = ['ROUTES']


def list_() -> JSON:
    """Lists user registrations."""

    return JSON([ur.to_json() for ur in get_user_registrations()])


@require_json(dict)
def accept(ident: int) -> JSONMessage:
    """Accept a registration."""

    user_registration = get_user_registration(ident)
    tenement = get_tenement(request.json.get('tenement'))
    user = user_registration.to_user(tenement)
    user.save()
    user_registration.notify(True)
    return JSONMessage('Added user.', id=user.id, status=201)


def deny(ident: int) -> JSONMessage:
    """Deny a registration."""

    user_registration = get_user_registration(ident)
    user_registration.delete_instance()
    user_registration.notify(False)
    return JSONMessage('User registration denied.', status=200)


ROUTES = [
    ('GET', '/registration', list_),
    ('POST', '/registration/<int:ident>', accept),
    ('DELETE', '/registration/<int:ident>', deny)
]
