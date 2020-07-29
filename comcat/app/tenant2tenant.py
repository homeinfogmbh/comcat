"""Tenant-to-tenant endpoint."""

from authlib.integrations.flask_oauth2 import current_token
from flask import request
from peewee import JOIN

from tenant2tenant import MESSAGE_ADDED, TenantMessage, Visibility
from wsgilib import JSON

from comcatlib.orm.tenant2tenant import UserTenantMessage


__all__ = ['ENDPOINTS']


def tenant_messages():
    """Yields the tenant-to-tenant messages the current user may access."""

    user = current_token.user

    if user.root:
        # Root users can see all tenant-to-tenant messages.
        return TenantMessage.select()

    if user.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        return TenantMessage.select().where(
            TenantMessage.customer == user.customer)

    condition = (
        # Own messages.
        (UserTenantMessage.issuer == user)
        | (
            # Show messages of the same customer
            # under the following conditions.
            (TenantMessage.customer == user.customer)
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
                    & (TenantMessage.address == user.tenement.address)
                )
            )
        )
    )
    select = TenantMessage.select().join(
        UserTenantMessage, join_type=JOIN.LEFT_OUTER)
    return select.where(condition)


def list_():
    """Lists all tenant-to-tenant messages."""

    return JSON([msg.to_json() for msg in tenant_messages()])


def post():
    """Adds a new tenant-to-tenant message."""

    tenant_message = TenantMessage.from_json(request.json)
    tenant_message.save()
    user_tenant_message = UserTenantMessage(
        tenant_message=tenant_message, user=current_token.user)
    user_tenant_message.save()
    return MESSAGE_ADDED.update(id=user_tenant_message.id)


ENDPOINTS = (
    (['GET'], '/tenant2tenant', list_),
    (['POST'], '/tenant2tenant', post)
)
