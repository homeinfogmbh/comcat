"""Tenements management."""

from typing import Union

from flask import request
from peewee import IntegrityError

from his import authenticated, authorized, root
from his.messages.customer import NO_SUCH_CUSTOMER
from mdb import Address, Customer, Tenement
from wsgilib import JSON, JSONMessage

from comcatlib.messages import INVALID_ADDRESS
from comcatlib.messages import NO_SUCH_ADDRESS
from comcatlib.messages import TENEMENT_ADDED
from comcatlib.messages import TENEMENT_DELETED
from comcatlib.messages import TENEMENT_IN_USE

from comcat.his.functions import get_tenement, get_tenements


__all__ = ['ROUTES']


def get_address(address: Union[int, dict]) -> Address:
    """Returns the specified address."""

    if isinstance(address, int):
        try:
            return Address[address]
        except Address.DoesNotExist:
            raise NO_SUCH_ADDRESS from None

    if isinstance(address, list):
        if len(address) != 4:
            raise INVALID_ADDRESS

        address = Address.add_by_address(address)

        if not address.id:
            address.save()

        return address

    raise INVALID_ADDRESS


def get_customer(ident: int) -> Customer:
    """Returns the specified customer."""

    try:
        return Customer[ident]
    except Customer.DoesNotExist:
        raise NO_SUCH_CUSTOMER from None


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists available tenements."""

    return JSON([tenement.to_json() for tenement in get_tenements()])


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Gets the respective tenement."""

    return JSON(get_tenement(ident).to_json())


@authenticated
@authorized('comcat')
@root
def add() -> JSONMessage:
    """Adds a tenement."""

    customer = get_customer(request.json.pop('customer'))
    address = get_address(request.json.pop('address'))
    tenement = Tenement.from_json(request.json, customer, address)
    tenement.save()
    return TENEMENT_ADDED.update(id=tenement.id)


@authenticated
@authorized('comcat')
@root
def delete(ident: int) -> JSONMessage:
    """Deletes a tenement."""

    tenement = get_tenement(ident)
    address = tenement.address

    try:
        tenement.delete_instance()
    except IntegrityError:
        return TENEMENT_IN_USE

    try:
        address.delete_instance()
    except IntegrityError:
        address_deleted = False
    else:
        address_deleted = True

    return TENEMENT_DELETED.update(address_deleted=address_deleted)


ROUTES = (
    ('GET', '/tenement', list_),
    ('GET', '/tenement/<int:ident>', get),
    ('POST', '/tenement', add),
    ('DELETE', '/tenement/<int:ident>', delete)
)
