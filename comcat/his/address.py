"""Address management."""

from flask import request

from comcatlib import Address
from comcatlib.messages import ADDRESS_ADDED, ADDRESS_DELETED, NO_SUCH_ADDRESS
from his import CUSTOMER, authenticated, authorized, root
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_():
    """Lists available addresses."""

    return JSON([address.to_json() for address in Address.select().where(
        Address.customer == CUSTOMER.id)])


@authenticated
@authorized('comcat')
@root
def add():
    """Adds a new address."""

    address = Address.from_json(request.json, CUSTOMER.id, unique=True)
    address.save()
    return ADDRESS_ADDED.update(id=address.id)


@authenticated
@authorized('comcat')
@root
def delete(ident):
    """Deletes an address."""

    try:
        address = Address.get(
            (Address.id == ident)
            & (Address.customer == CUSTOMER.id))
    except Address.DoesNotExist:
        return NO_SUCH_ADDRESS

    address.delete_instance()
    return ADDRESS_DELETED


ROUTES = (
    ('GET', '/address', list_, 'list_addresses'),
    ('POST', '/address', add, 'add_address'),
    ('DELETE', '/address/<int:ident>', delete, 'delete_address'))
