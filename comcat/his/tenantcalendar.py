"""Customer-oriented HIS backend."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_datetime

from tenantcalendar.errors import ERRORS
from tenantcalendar.functions import list_customer_events
from tenantcalendar.functions import get_customer_event
from tenantcalendar.functions import list_user_events
from tenantcalendar.functions import get_user_event
from tenantcalendar.orm import CustomerEvent, UserEvent


__all__ = ['ERRORS', 'ROUTES']


CUSTOMER_FIELDS = {'title', 'start', 'end', 'text'}
USER_FIELDS = {'title', 'email', 'phone', 'start', 'end', 'text'}


@authenticated
@authorized('comcat')
def _list_customer_events() -> JSON:
    """Lists customer events."""

    return JSON([
        customer_event.to_json() for customer_event in list_customer_events(
            CUSTOMER.id, start=get_datetime('start'), end=get_datetime('end'))
    ])


@authenticated
@authorized('comcat')
def _list_user_events() -> JSON:
    """Lists user events."""

    return JSON([user_event.to_json() for user_event in list_user_events(
        CUSTOMER.id, start=get_datetime('start'), end=get_datetime('end'))])


@authenticated
@authorized('comcat')
def add_customer_event() -> JSONMessage:
    """Adds a customer event."""

    customer_event = CustomerEvent.from_json(
        request.json, CUSTOMER.id, only=CUSTOMER_FIELDS)
    customer_event.save()
    return JSONMessage('Customer event added.', id=customer_event.id,
                       status=201)


@authenticated
@authorized('comcat')
def patch_customer_event(ident: int) -> JSONMessage:
    """Patches a customer event."""

    try:
        customer_event = get_customer_event(ident, CUSTOMER.id)
    except CustomerEvent.DoesNotExist:
        return JSONMessage('No such customer event.', status=404)

    customer_event.patch_json(request.json, only=CUSTOMER_FIELDS)
    customer_event.save()
    return JSONMessage('Customer event patched.', status=200)


@authenticated
@authorized('comcat')
def patch_user_event(ident: int) -> JSONMessage:
    """Patches a user event."""

    try:
        user_event = get_user_event(ident, CUSTOMER.id)
    except UserEvent.DoesNotExist:
        return JSONMessage('No such user event.', status=404)

    user_event.patch_json(request.json, only=USER_FIELDS)
    user_event.save()
    return JSONMessage('User event patched.', status=200)


@authenticated
@authorized('comcat')
def delete_customer_event(ident: int) -> JSONMessage:
    """Deletes a customer event."""

    try:
        customer_event = get_customer_event(ident, CUSTOMER.id)
    except CustomerEvent.DoesNotExist:
        return JSONMessage('No such customer event.', status=404)

    customer_event.delete_instance()
    return JSONMessage('Customer event deleted.', status=200)


@authenticated
@authorized('comcat')
def delete_user_event(ident: int) -> JSONMessage:
    """Deletes a user event."""

    try:
        user_event = get_user_event(ident, CUSTOMER.id)
    except UserEvent.DoesNotExist:
        return JSONMessage('No such user event.', status=404)

    user_event.delete_instance()
    return JSONMessage('User event deleted.', status=200)


ROUTES = [
    ('GET', '/tenantcalendar/customer', _list_customer_events),
    ('GET', '/tenantcalendar/user', _list_user_events),
    ('POST', '/tenantcalendar/customer', add_customer_event),
    ('PATCH', '/tenantcalendar/customer/<int:ident>', patch_customer_event),
    ('PATCH', '/tenantcalendar/user/<int:ident>', patch_user_event),
    ('DELETE', '/tenantcalendar/customer/<int:ident>', delete_customer_event),
    ('DELETE', '/tenantcalendar/user/<int:ident>', delete_user_event)
]
