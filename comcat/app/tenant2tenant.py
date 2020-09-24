"""Tenant-to-tenant endpoint."""

from datetime import datetime

from flask import request
from peewee import JOIN

from tenant2tenant import MESSAGE_ADDED
from tenant2tenant import MESSAGE_DELETED
from tenant2tenant import NO_SUCH_MESSAGE
#from tenant2tenant import email
from tenant2tenant import Configuration
from tenant2tenant import TenantMessage
from tenant2tenant import Visibility
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH, USER
from comcatlib.orm.tenant2tenant import UserTenantMessage


__all__ = ['ENDPOINTS']


def _get_messages():
    """Yields the tenant-to-tenant messages the current user may access."""

    if USER.root:
        # Root users can see all tenant-to-tenant messages.
        return TenantMessage.select()

    if USER.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        return TenantMessage.select().where(
            TenantMessage.customer == USER.customer)

    condition = (
        (UserTenantMessage.user == USER.id)
        | (
            # Show messages of the same customer
            # under the following conditions.
            (TenantMessage.customer == USER.customer)
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
                    & (TenantMessage.address == USER.tenement.address)
                )
            )
        )
    )
    select = TenantMessage.select().join(UserTenantMessage, JOIN.LEFT_OUTER)
    return select.where(condition)


def _get_deletable_message(ident):
    """Returns a tenant-to-tenant message
    that the current user may delete.
    """

    if USER.root:
        try:
            return TenantMessage[ident]
        except TenantMessage.DoesNotExist:
            raise NO_SUCH_MESSAGE

    condition = TenantMessage.customer == USER.customer
    condition &= TenantMessage.id == ident

    if USER.admin:
        try:
            return TenantMessage.select().where(condition).get()
        except TenantMessage.DoesNotExist:
            raise NO_SUCH_MESSAGE


    condition &= UserTenantMessage.user == USER.id
    select = TenantMessage.select().join(UserTenantMessage)

    try:
        return select.where(condition).get()
    except TenantMessage.DoesNotExist:
        raise NO_SUCH_MESSAGE


def _add_message():
    """Adds a tenant message."""

    customer = USER.customer
    address = USER.tenement.address
    message = request.json['message']
    tenant_message = TenantMessage.add(customer, address, message)
    tenant_message.subject = request.json.get('subject') or None
    visibility = request.json.get('visibility')

    if visibility:
        tenant_message.visibility = Visibility(visibility)
    else:
        tenant_message.visibility = Visibility.TENEMENT

    configuration = Configuration.for_customer(customer)

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
    return MESSAGE_ADDED.update(id=tenant_message.id)


@REQUIRE_OAUTH('comcat')
def delete(ident):
    """Deletes a tenant-to-tenant message."""

    _get_deletable_message(ident).delete_instance()
    return MESSAGE_DELETED


ENDPOINTS = (
    (['GET'], '/tenant2tenant', list_),
    (['POST'], '/tenant2tenant', post),
    (['DELETE'], '/tenant2tenant/<int:ident>', delete)
)
