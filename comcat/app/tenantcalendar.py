"""Tenant calendar endpoint."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, TENEMENT
from tenantcalendar import ERRORS
from tenantcalendar import UserEvent
from tenantcalendar import list_customer_events
from tenantcalendar import list_user_events
from tenantcalendar import get_own_event
from wsgilib import JSON, JSONMessage, get_datetime


__all__ = ['ROUTES', 'ERRORS']


CUSTOMER_FIELDS = {'title', 'start', 'end', 'text'}


@REQUIRE_OAUTH('comcat')
def _list_customer_events() -> JSON:
    """Lists customer events."""

    return JSON([
        customer_event.to_json() for customer_event in list_customer_events(
            TENEMENT.customer, start=get_datetime('start'),
            end=get_datetime('end')
        )
    ])


@REQUIRE_OAUTH('comcat')
def _list_user_events() -> JSON:
    """Lists user events."""

    return JSON([
        user_event.to_json() for user_event in list_user_events(
            TENEMENT.customer, start=get_datetime('start'),
            end=get_datetime('end')
        )
    ])


@REQUIRE_OAUTH('comcat')
def add_user_event() -> JSONMessage:
    """Adds a user event."""

    user_event = UserEvent.from_json(
        request.json, USER.id, only=CUSTOMER_FIELDS)
    user_event.save()
    return JSONMessage('User event added.', id=user_event.id, status=201)


@REQUIRE_OAUTH('comcat')
def patch_user_event(ident: int) -> JSONMessage:
    """Patches an event."""

    user_event = get_own_event(ident, USER.id)
    user_event.patch_json(request.json, only=CUSTOMER_FIELDS)
    user_event.save()
    return JSONMessage('User event patched.', status=200)


@REQUIRE_OAUTH('comcat')
def delete_user_event(ident: int) -> JSONMessage:
    """Deletes an event."""

    get_own_event(ident, USER.id).delete_instance()
    return JSONMessage('Event deleted.', status=200)


ROUTES = [
    ('GET', '/tenantcalendar/customer-events', _list_customer_events),
    ('GET', '/tenantcalendar/user-events', _list_user_events),
    ('POST', '/tenantcalendar', add_user_event),
    ('PATCH', '/tenantcalendar/<int:ident>', patch_user_event),
    ('DELETE', '/tenantcalendar/<int:ident>', delete_user_event)
]
