"""Tenant-to-tenant endpoint."""

from datetime import datetime

from flask import request
from peewee import JOIN, ModelSelect

from tenant2tenant import Configuration
from tenant2tenant import TenantMessage
from tenant2tenant import Visibility
from wsgilib import JSON, JSONMessage

from comcatlib import ADDRESS
from comcatlib import CUSTOMER
from comcatlib import DATABASE
from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import User
from comcatlib import UserTenantMessage


__all__ = ['ENDPOINTS']


def _get_messages() -> ModelSelect:
    """Yields the tenant-to-tenant messages the current user may access."""

    select = TenantMessage.select(cascade=True).join_from(
        TenantMessage, UserTenantMessage, JOIN.LEFT_OUTER).join(
        User, JOIN.LEFT_OUTER)

    if USER.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        return select.where(TenantMessage.customer == CUSTOMER.id)

    condition = (
        # Always allow own messages.
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
                    # show entries of the same address.
                    (TenantMessage.visibility == Visibility.TENEMENT)
                    & (TenantMessage.address == ADDRESS.id)
                )
            )
        )
    )
    return select.where(condition).execute(DATABASE)


def _get_deletable_message(ident: int) -> ModelSelect:
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


def _add_message() -> TenantMessage:
    """Adds a tenant message."""

    message = request.json['message']
    tenant_message = TenantMessage.add(CUSTOMER.id, ADDRESS.id, message)
    tenant_message.subject = request.json.get('subject')
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
    return tenant_message


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists all tenant-to-tenant messages."""

    return JSON([msg.to_json() for msg in _get_messages()])


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Adds a new tenant-to-tenant message."""

    tenant_message = _add_message()
    user_tenant_message = UserTenantMessage(
        tenant_message=tenant_message, user=USER.id)
    user_tenant_message.save()
    return JSONMessage('Tenant message added.', id=tenant_message.id,
                       status=201)


@REQUIRE_OAUTH('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes a tenant-to-tenant message."""

    _get_deletable_message(ident).delete_instance()
    return JSONMessage('Tenant message deleted.', status=200)


ENDPOINTS = [
    (['GET'], '/tenant2tenant', list_, 'list_tenant2tenant_messages'),
    (['POST'], '/tenant2tenant', post, 'add_tenant2tenant_message'),
    (['DELETE'], '/tenant2tenant/<int:ident>', delete,
     'delete_tenant2tenant_message')
]
