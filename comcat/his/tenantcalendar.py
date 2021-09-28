"""HIS administration interface."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from tenantcalendar import ERRORS, list_events, get_event
from wsgilib import JSON, JSONMessage, get_datetime


__all__ = ['ROUTES', 'ERRORS']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """List events."""

    return JSON([event.to_json() for event in list_events(
        CUSTOMER.id, start=get_datetime('start'), end=get_datetime('end'))
    ])


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes an event."""

    get_event(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Event deleted.', status=200)


@authenticated
@authorized('comcat')
def patch(ident: int) -> JSONMessage:
    """Edits an event."""

    event = get_event(ident, CUSTOMER.id).patch_json(request.json)
    event.save()
    return JSONMessage('Event patched.', status=200)


ROUTES = [
    ('GET', '/tenantcalendar', list_),
    ('DELETE', '/tenantcalendar/<int:ident>', delete),
    ('PATCH', '/tenantcalendar/<int:ident>', patch)
]
