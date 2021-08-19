"""Tenant-to-tenant endpoint."""

from flask import request

from wsgilib import JSON, JSONMessage

from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import add_user_tenant_message
from comcatlib import get_deletable_tenant_message
from comcatlib import get_tenant_messages
from comcatlib import jsonify_tenant_message


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists all tenant-to-tenant messages."""

    user = USER._get_current_object()   # pylint: disable=W0212
    tenant_messages = get_tenant_messages(user)
    return JSON([jsonify_tenant_message(msg) for msg in tenant_messages])


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Adds a new tenant-to-tenant message."""

    user = USER._get_current_object()   # pylint: disable=W0212
    user_tenant_message = add_user_tenant_message(request.json, user)
    return JSONMessage('Tenant message added.', id=user_tenant_message.id,
                       status=201)


@REQUIRE_OAUTH('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes a tenant-to-tenant message."""

    user = USER._get_current_object()   # pylint: disable=W0212
    get_deletable_tenant_message(user, ident).delete_instance()
    return JSONMessage('Tenant message deleted.', status=200)


ENDPOINTS = [
    (['GET'], '/tenant2tenant', list_, 'list_tenant2tenant_messages'),
    (['POST'], '/tenant2tenant', post, 'add_tenant2tenant_message'),
    (['DELETE'], '/tenant2tenant/<int:ident>', delete,
     'delete_tenant2tenant_message')
]
