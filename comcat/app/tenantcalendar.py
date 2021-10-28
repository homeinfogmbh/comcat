"""Tenant calendar endpoint."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, TENEMENT
from tenantcalendar import ERRORS, Event, list_events, get_event
from wsgilib import JSON, JSONMessage, get_datetime


__all__ = ['ROUTES', 'ERRORS']


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists events."""

    return JSON([event.to_json() for event in list_events(
        TENEMENT.customer, start=get_datetime('start'),
        end=get_datetime('end'))
    ])


@REQUIRE_OAUTH('comcat')
def add() -> JSONMessage:
    """Adds an event."""

    event = Event.from_json(request.json, USER.id)
    event.save()
    return JSONMessage('Event added.', id=event.id, status=201)


@REQUIRE_OAUTH('comcat')
def patch(ident: int) -> JSONMessage:
    """Patches an event."""

    event = get_event(ident, TENEMENT.customer).patch_json(request.json)
    event.save()
    return JSONMessage('Event patched.', status=200)


@REQUIRE_OAUTH('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes an event."""

    get_event(ident, TENEMENT.customer).delete_instance()
    return JSONMessage('Event deleted.', status=200)


ROUTES = [
    ('GET', '/tenantcalendar', list_),
    ('POST', '/tenantcalendar', add),
    ('PATCH', '/tenantcalendar/<int:ident>', patch),
    ('DELETE', '/tenantcalendar/<int:ident>', delete)
]
