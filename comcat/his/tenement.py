"""Tenements management."""

from flask import request
from peewee import IntegrityError

from his import CUSTOMER, authenticated, authorized
from mdb import Tenement
from wsgilib import JSON, JSONMessage

from comcat.his.functions import get_address
from comcat.his.functions import get_customer
from comcat.his.functions import get_tenement
from comcat.his.functions import get_tenements


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists available tenements."""

    return JSON([
        tenement.to_json() for tenement in get_tenements(CUSTOMER.id)
    ])


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Gets the respective tenement."""

    return JSON(get_tenement(ident, CUSTOMER.id).to_json())


@authenticated
@authorized('comcat')
def add() -> JSONMessage:
    """Adds a tenement."""

    customer = get_customer(request.json.pop('customer'))
    address = get_address(request.json.pop('address'))
    tenement = Tenement.from_json(request.json, customer, address)
    tenement.save()
    return JSONMessage('Tenement added.', id=tenement.id, status=201)


@authenticated
@authorized('comcat')
def patch(ident: int) -> JSONMessage:
    """Modifies a tenement."""

    tenement = get_tenement(ident, CUSTOMER.id)

    if (address := request.json.pop('address', None)) is not None:
        tenement.address = get_address(address)

    tenement.patch_json(request.json)
    tenement.save()
    return JSONMessage('Tenement patched.', status=200)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes a tenement."""

    tenement = get_tenement(ident, CUSTOMER.id)
    address = tenement.address

    try:
        tenement.delete_instance()
    except IntegrityError:
        return JSONMessage('The tenement is in use.', status=400)

    try:
        address.delete_instance()
    except IntegrityError:
        address_deleted = False
    else:
        address_deleted = True

    return JSONMessage(
        'Tenement deleted.', address_deleted=address_deleted, status=200
    )


ROUTES = [
    ('GET', '/tenement', list_),
    ('GET', '/tenement/<int:ident>', get),
    ('POST', '/tenement', add),
    ('PATCH', '/tenement/<int:ident>', patch),
    ('DELETE', '/tenement/<int:ident>', delete)
]
