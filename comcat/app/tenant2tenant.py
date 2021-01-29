"""Tenant-to-tenant endpoint."""

from datetime import datetime

from flask import request
from peewee import JOIN

#from tenant2tenant import email
from tenant2tenant import Configuration
from tenant2tenant import TenantMessage
from tenant2tenant import Visibility
from wsgilib import JSON, JSONMessage

from comcatlib import ADDRESS, CUSTOMER, REQUIRE_OAUTH, USER
from comcatlib.orm.tenant2tenant import UserTenantMessage


__all__ = ['ENDPOINTS']


def _get_messages():
    """Yields the tenant-to-tenant messages the current user may access."""

    select = TenantMessage.select(cascade=True).join_from(
        TenantMessage, UserTenantMessage, JOIN.LEFT_OUTER)

    if USER.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        return select.where(TenantMessage.customer == CUSTOMER.id)

    condition = (
        (UserTenantMessage.user == USER.id)
        | (
            # Show messages of the same customer
            # under the following conditions.
            (TenantMessage.customer == CUSTOMER.id)
            # Only show released messages.
            & (TenantMessage.released == 1)
            & (
                (
                    # If the visibility is set to customer-wide,
                    # show all those entries of the same customer.
                    TenantMessage.visibility == Visibility.CUSTOMER
                ) | (
                    # If the visibility is restricted to tenement, only
                    # show entries of the same customer and address.
                    (TenantMessage.visibility == Visibility.TENEMENT)
                    & (TenantMessage.address == ADDRESS.id)
                )
            )
        )
    )
    return select.where(condition)


def _get_deletable_message(ident):
    """Returns a tenant-to-tenant message
    that the current user may delete.
    """

    condition = TenantMessage.customer == CUSTOMER.id
    condition &= TenantMessage.id == ident

    if USER.admin:
        return TenantMessage.select().where(condition).get()


    condition &= UserTenantMessage.user == USER.id
    select = TenantMessage.select().join(UserTenantMessage)
    return select.where(condition).get()


def _add_message():
    """Adds a tenant message."""

    message = request.json['message']
    tenant_message = TenantMessage.add(CUSTOMER.id, ADDRESS.id, message)
    tenant_message.subject = request.json.get('subject') or None
    visibility = request.json.get('visibility')

    if visibility:
        tenant_message.visibility = Visibility(visibility)
    else:
        tenant_message.visibility = Visibility.TENEMENT

    configuration = Configuration.for_customer(CUSTOMER.id)

    if configuration.auto_release:
        tenant_message.released = True
        tenant_message.start_date = now = datetime.now()
        tenant_message.end_date = now + configuration.release_time

    tenant_message.save()
    #email(tenant_message)  # Notify customer about new message.
    return tenant_message


@REQUIRE_OAUTH('comcat')
def list_():
    """Lists all tenant-to-tenant messages."""

    return JSON([msg.to_json() for msg in _get_messages()])


@REQUIRE_OAUTH('comcat')
def post():
    """Adds a new tenant-to-tenant message."""

    tenant_message = _add_message()
    user_tenant_message = UserTenantMessage(
        tenant_message=tenant_message, user=USER.id)
    user_tenant_message.save()
    return JSONMessage('Tenant message added.', id=tenant_message.id,
                       status=201)


@REQUIRE_OAUTH('comcat')
def delete(ident):
    """Deletes a tenant-to-tenant message."""

    _get_deletable_message(ident).delete_instance()
    return JSONMessage('Tenant message deleted.', status=200)


ENDPOINTS = [
    (['GET'], '/tenant2tenant', list_, 'list_tenant2tenant_messages'),
    (['POST'], '/tenant2tenant', post, 'add_tenant2tenant_message'),
    (['DELETE'], '/tenant2tenant/<int:ident>', delete,
     'delete_tenant2tenant_message')
]
