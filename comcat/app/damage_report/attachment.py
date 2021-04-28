"""Damage report endpoints."""

from flask import request

from comcatlib import REQUIRE_OAUTH
from damage_report import Attachment
from filedb import File
from wsgilib import JSONMessage

from comcat.app.functions import get_attachment
from comcat.app.functions import get_user_damage_report


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def post(ident: int) -> JSONMessage:
    """Adds an attachment for the given damage report."""

    bytes_ = request.get_data()
    user_damage_report = get_user_damage_report(ident)
    damage_report = user_damage_report.damage_report
    file = File.from_bytes(bytes_)
    file.save()
    attachment = Attachment(damage_report=damage_report, file=file)
    attachment.save()
    return JSONMessage('Attachment added.', id=attachment.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete(attachment_id: int) -> JSONMessage:
    """Removes the respective attachment."""

    attachment = get_attachment(attachment_id)
    attachment.delete_instance()
    return JSONMessage('Attachment deleted.', status=200)


ENDPOINTS = (
    (['POST'], '/damage-report/attachment/<int:ident>', post,
     'add_damage_report_attachment'),
    (['DELETE'], '/damage-report/attachment/<int:attachment_id>', delete,
     'delete_damage_report_attachment')
)
