"""Marketplace interface."""

from flask import request
from peewee import IntegrityError

from comcatlib import REQUIRE_OAUTH, TENEMENT, USER
from marketplace import ERRORS
from marketplace import add_offer
from marketplace import get_offer
from marketplace import get_offers
from marketplace import add_image
from marketplace import get_image
from wsgilib import Binary, JSON, JSONMessage


__all__ = ["ROUTES", "ERRORS"]


@REQUIRE_OAUTH("comcat")
def list_() -> JSON:
    """Lists available offers."""

    offers = get_offers(customer=TENEMENT.customer)
    return JSON([offer.to_json() for offer in offers])


@REQUIRE_OAUTH("comcat")
def get(ident: int) -> JSON:
    """Returns the respective offer."""

    offer = get_offer(ident, customer=TENEMENT.customer)
    return JSON(offer.to_json())


@REQUIRE_OAUTH("comcat")
def add() -> JSONMessage:
    """Adds a new offer."""

    offer = add_offer(request.json, USER.id)
    return JSONMessage("Offer added.", id=offer.id, status=201)


@REQUIRE_OAUTH("comcat")
def delete(ident: int) -> JSONMessage:
    """Deletes an offer."""

    offer = get_offer(ident, user=USER.id)
    offer.delete_instance()
    return JSONMessage("Offer deleted.", status=200)


@REQUIRE_OAUTH("comcat")
def get_img(ident: int) -> Binary:
    """Returns an Image."""

    image = get_image(ident, customer=TENEMENT.customer)
    return Binary(image.file.bytes)


@REQUIRE_OAUTH("comcat")
def add_img(offer: int, index: int) -> JSONMessage:
    """Adds an Image."""

    offer = get_offer(offer, user=USER.id)

    try:
        image = add_image(offer, request.get_data(), index)
    except IntegrityError as error:
        code, msg = error.args
        return JSONMessage("Integrity error.", code=code, msg=msg, status=500)

    return JSONMessage("Image added.", id=image.id, status=201)


@REQUIRE_OAUTH("comcat")
def delete_img(ident: int) -> JSONMessage:
    """Deletes an Image."""

    get_image(ident, user=USER.id).delete_instance()
    return JSONMessage("image deleted.", status=200)


ROUTES = [
    (["GET"], "/marketplace", list_),
    (["GET"], "/marketplace/<int:ident>", get),
    (["POST"], "/marketplace", add),
    (["DELETE"], "/marketplace/<int:ident>", delete),
    (["GET"], "/marketplace/image/<int:ident>", get_img),
    (["POST"], "/marketplace/<int:offer>/image/<int:index>", add_img),
    (["DELETE"], "/marketplace/image/<int:ident>", delete_img),
]
