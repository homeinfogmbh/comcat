"""Damage report endpoints."""

from flask import request

from comcatlib import REQUIRE_OAUTH
from damage_report import Attachment
from filedb import File
from wsgilib import Binary, JSONMessage

from comcat.functions import get_attachment
from comcat.functions import get_user_damage_report


__all__ = ["ROUTES"]


@REQUIRE_OAUTH("comcat")
def get(ident: int) -> Binary:
    """Returns the respective attachment data."""

    attachment = get_attachment(ident)
    return Binary(attachment.file.bytes)


@REQUIRE_OAUTH("comcat")
def post(ident: int) -> JSONMessage:
    """Adds an attachment for the given damage report."""

    bytes_ = request.get_data()
    user_damage_report = get_user_damage_report(ident)
    damage_report = user_damage_report.damage_report
    file = File.from_bytes(bytes_)
    file.save()
    attachment = Attachment(damage_report=damage_report, file=file)
    attachment.save()
    return JSONMessage("Attachment added.", id=attachment.id, status=201)


@REQUIRE_OAUTH("comcat")
def delete(ident: int) -> JSONMessage:
    """Removes the respective attachment."""

    attachment = get_attachment(ident)
    attachment.delete_instance()
    return JSONMessage("Attachment deleted.", status=200)


ROUTES = (
    (["GET"], "/damage-report/attachment/<int:ident>", get),
    (["POST"], "/damage-report/<int:ident>/attachment", post),
    (["DELETE"], "/damage-report/attachment/<int:ident>", delete),
)
