"""Tenement management."""

from flask import request

from comcatlib import Tenement
from comcatlib.messages import NO_SUCH_TENEMENT
from comcatlib.messages import TENEMENT_ADDED
from comcatlib.messages import TENEMENT_DELETED
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_():
    """Lists available tenements."""

    return JSON([tenement.to_json() for tenement in Tenement.select().where(
        Tenement.customer == CUSTOMER.id)])


@authenticated
@authorized('comcat')
def add():
    """Adds a new tenement."""

    tenement = Tenement.from_json(request.json, CUSTOMER.id)
    tenement.save()
    return TENEMENT_ADDED.update(id=tenement.id)


@authenticated
@authorized('comcat')
def delete(ident):
    """Deletes a tenement."""

    try:
        tenement = Tenement.get(
            (Tenement.id == ident)
            & (Tenement.customer == CUSTOMER.id))
    except Tenement.DoesNotExist:
        return NO_SUCH_TENEMENT

    tenement.delete_instance()
    return TENEMENT_DELETED


ROUTES = (
    ('GET', '/tenement', list_, 'list_tenements'),
    ('POST', '/tenement', add, 'add_tenements'),
    ('DELETE', '/tenement/<int:ident>', delete, 'delete_tenements'))
