"""ORM-related functions."""

from authlib.integrations.flask_oauth2 import current_token
from peewee import JOIN

from tenant2tenant import TenantMessage, Visibility
from wsgilib import JSON

from comcatlib.orm.tenant2tenant import UserTenantMessage
from comcatlib.orm.user import User


__all__ = ['ENDPOINTS']


def tenant_messages():
    """Yields the tenant-to-tenant messages the current user may access."""

    user = current_token.user

    if user.root:
        # Root users can see all tenant-to-tenant messages.
        return TenantMessage.select()

    if user.admin:
        # Admins can see all tenant-to-tenant messages of their company.
        condition = User.customer == user.customer
        select = TenantMessage.join(UserTenantMessage).join(User)
        return select.where(condition)

    condition = (
        # Own messages.
        (UserTenantMessage.issuer == user)
        | (
            # Show messages of the same customer
            # under the following conditions.
            (TenantMessage.customer == user.customer)
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


ENDPOINTS = (
    (['GET'], '/tenant2tenant', list_),
)
