"""Handles user tenant messages."""

from his import authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_user_tenant_messages


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists user tenant messages."""

    return JSON([utm.to_json() for utm in get_user_tenant_messages()])


ROUTES = [('GET', '/tenant2tenant', list_)]
