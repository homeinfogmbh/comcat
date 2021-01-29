"""Damage report endpoints."""

from flask import request

from comcatlib import REQUIRE_OAUTH
from damage_report import Attachment
from wsgilib import JSONMessage

from comcat.app.user_files import get_user_file
from comcat.app.functions import get_attachment, get_user_damage_report


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Adds an attachment for the given damage report."""

    user_damage_report = get_user_damage_report(
        request.json.pop('userDamageReport'))
    user_file = get_user_file(request.json.pop('file'))
    attachment = Attachment(
        damage_report=user_damage_report.damage_report, file=user_file.file)
    attachment.save()
    return JSONMessage('Attachment added.', id=attachment.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete(attachment_id: int) -> JSONMessage:
    """Removes the respective attachment."""

    attachment = get_attachment(attachment_id)
    attachment.delete_instance()
    return JSONMessage('Attachment deleted.', status=200)


ENDPOINTS = (
    (['POST'], '/damage-report/attachment', post,
     'add_damage_report_attachment'),
    (['DELETE'], '/damage-report/attachment/<int:attachment_id>', delete,
     'delete_damage_report_attachment')
)
