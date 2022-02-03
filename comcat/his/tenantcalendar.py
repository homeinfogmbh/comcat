"""Customer-oriented HIS backend."""

from flask import request

from cmslib import get_deployment, get_group
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_datetime

from tenantcalendar import ERRORS
from tenantcalendar import add_to_deployment
from tenantcalendar import add_to_group
from tenantcalendar import add_to_user
from tenantcalendar import get_customer_event
from tenantcalendar import get_deployment_customer_event
from tenantcalendar import get_deployment_customer_events
from tenantcalendar import get_group_customer_event
from tenantcalendar import get_group_customer_events
from tenantcalendar import get_user_customer_event
from tenantcalendar import get_user_customer_events
from tenantcalendar import get_user_event
from tenantcalendar import list_customer_events
from tenantcalendar import list_user_events
from tenantcalendar import CustomerEvent
from tenantcalendar import DeploymentCustomerEvent
from tenantcalendar import GroupCustomerEvent
from tenantcalendar import UserCustomerEvent
from tenantcalendar import UserEvent

from comcat.his.functions import get_user


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
        CUSTOMER.id, start=get_datetime('start'), end=get_datetime('end')
    )])


@authenticated
@authorized('comcat')
def add_customer_event() -> JSONMessage:
    """Adds a customer event."""

    customer_event = CustomerEvent.from_json(
        request.json, CUSTOMER.id, only=CUSTOMER_FIELDS
    )
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


@authenticated
@authorized('comcat')
def list_deployment_memberships() -> JSON:
    """List deployment memberships."""

    return JSON([
        dce.to_json() for dce in get_deployment_customer_events(CUSTOMER.id)
    ])


@authenticated
@authorized('comcat')
def list_group_memberships() -> JSON:
    """List group memberships."""

    return JSON([
        gce.to_json() for gce in get_group_customer_events(CUSTOMER.id)
    ])


@authenticated
@authorized('comcat')
def list_user_memberships() -> JSON:
    """List user memberships."""

    return JSON([
        uce.to_json() for uce in get_user_customer_events(CUSTOMER.id)
    ])


@authenticated
@authorized('comcat')
def add_deployment_membership() -> JSONMessage:
    """Add a deployment membership."""

    dce = add_to_deployment(
        get_customer_event(request.json['event'], CUSTOMER.id),
        get_deployment(request.json['deployment'])
    )
    return JSONMessage('Event added to deployment.', id=dce.id, status=201)


@authenticated
@authorized('comcat')
def add_group_membership() -> JSONMessage:
    """Add a group membership."""

    gce = add_to_group(
        get_customer_event(request.json['event'], CUSTOMER.id),
        get_group(request.json['group'])
    )
    return JSONMessage('Event added to group.', id=gce.id, status=201)


@authenticated
@authorized('comcat')
def add_user_membership() -> JSONMessage:
    """Add a user membership."""

    uce = add_to_user(
        get_customer_event(request.json['event'], CUSTOMER.id),
        get_user(request.json['user'])
    )
    return JSONMessage('Event added to user.', id=uce.id, status=201)


@authenticated
@authorized('comcat')
def remove_deployment_membership(ident: int) -> JSONMessage:
    """Remove a deployment membership."""

    try:
        dce = get_deployment_customer_event(ident, CUSTOMER.id)
    except DeploymentCustomerEvent.DoesNotExist:
        return JSONMessage('Event not member of deployment.', status=400)

    dce.delete_instance()
    return JSONMessage('Event removed from deployment.', status=200)


@authenticated
@authorized('comcat')
def remove_group_membership(ident: int) -> JSONMessage:
    """Remove a group membership."""

    try:
        gce = get_group_customer_event(ident, CUSTOMER.id)
    except GroupCustomerEvent.DoesNotExist:
        return JSONMessage('Event not member of group.', status=400)

    gce.delete_instance()
    return JSONMessage('Event removed from group.', status=200)


@authenticated
@authorized('comcat')
def remove_user_membership(ident: int) -> JSONMessage:
    """Remove a user membership."""

    try:
        uce = get_user_customer_event(ident, CUSTOMER.id)
    except UserCustomerEvent.DoesNotExist:
        return JSONMessage('Event not member of user.', status=400)

    uce.delete_instance()
    return JSONMessage('Event removed from user.', status=200)


ROUTES = [
    ('GET', '/tenantcalendar/customer', _list_customer_events),
    ('GET', '/tenantcalendar/user', _list_user_events),
    ('GET', '/tenantcalendar/membership/deployment',
     list_deployment_memberships),
    ('GET', '/tenantcalendar/membership/group', list_group_memberships),
    ('GET', '/tenantcalendar/membership/user', list_user_memberships),
    ('POST', '/tenantcalendar/customer', add_customer_event),
    ('POST', '/tenantcalendar/membership/deployment',
     add_deployment_membership),
    ('POST', '/tenantcalendar/membership/group', add_group_membership),
    ('POST', '/tenantcalendar/membership/user', add_user_membership),
    ('PATCH', '/tenantcalendar/customer/<int:ident>', patch_customer_event),
    ('PATCH', '/tenantcalendar/user/<int:ident>', patch_user_event),
    ('DELETE', '/tenantcalendar/customer/<int:ident>', delete_customer_event),
    ('DELETE', '/tenantcalendar/user/<int:ident>', delete_user_event),
    ('DELETE', '/tenantcalendar/membership/deployment/<int:ident>',
     remove_deployment_membership),
    ('DELETE', '/tenantcalendar/membership/group/<int:ident>',
     remove_group_membership),
    ('DELETE', '/tenantcalendar/membership/user/<int:ident>',
     remove_group_membership)
]
