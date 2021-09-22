"""Marketplace interface."""

from flask import request

from comcatlib import REQUIRE_OAUTH, TENEMENT, USER
from marketplace import ImageTooLarge
from marketplace import InvalidPrice
from marketplace import MaxImagesReached
from marketplace import add_offer
from marketplace import get_offer
from marketplace import get_offers
from marketplace import add_image
from marketplace import get_image
from wsgilib import Binary, JSON, JSONMessage


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists avilable offers."""

    offers = get_offers(customer=TENEMENT.customer)
    return JSON([offer.to_json() for offer in offers])


@REQUIRE_OAUTH('comcat')
def get(ident: int) -> JSON:
    """Returns the respective offer."""

    offer = get_offer(ident, customer=TENEMENT.customer)
    return JSON(offer.to_json())


@REQUIRE_OAUTH('comcat')
def add() -> JSONMessage:
    """Adds a new offer."""

    try:
        offer = add_offer(request.json, USER.id)
    except InvalidPrice:
        return JSONMessage('Invalid price.', status=400)

    return JSONMessage('Offer added.', id=offer.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes an offer."""

    offer = get_offer(ident, user=USER.id)
    offer.delete_instance()
    return JSONMessage('Offer deleted.', status=200)


@REQUIRE_OAUTH('comcat')
def get_img(ident: int) -> Binary:
    """Returns an Image."""

    image = get_image(ident, customer=TENEMENT.customer)
    return Binary(image.file.bytes)


@REQUIRE_OAUTH('comcat')
def add_img(offer: int, index: int) -> JSONMessage:
    """Adds an Image."""

    offer = get_offer(offer, user=USER.id)

    try:
        add_image(offer, request.get_data(), index)
    except ImageTooLarge:
        return JSONMessage('Image too large.', status=400)
    except MaxImagesReached:
        return JSONMessage('Maximum amount of images reached.', status=400)

    return JSONMessage('Image added.', status=201)


@REQUIRE_OAUTH('comcat')
def delete_img(ident: int) -> JSONMessage:
    """Deletes an Image."""

    get_image(ident, user=USER.id).delete_instance()
    return JSONMessage('image deleted.', status=200)


ENDPOINTS = [
    (['GET'], '/marketplace', list_, 'list_offers'),
    (['GET'], '/marketplace/<int:ident>', get, 'get_offer'),
    (['POST'], '/marketplace', add, 'add_offer'),
    (['DELETE'], '/marketplace/<int:ident>', delete, 'delete_offer'),
    (['GET'], '/marketplace/image/<int:ident>', get_img, 'get_image'),
    (['POST'], '/marketplace/<int:offer>/image/<int:index>', add_img,
     'add_image'),
    (['DELETE'], '/marketplace/image/<int:ident>', delete_img, 'delete_image')
]
