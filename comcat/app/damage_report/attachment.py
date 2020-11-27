"""Damage report endpoints."""

from typing import Iterable

from flask import request

from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import User
from comcatlib import UserDamageReport
from comcatlib.messages import ATTACHMENT_ADDED
from comcatlib.messages import ATTACHMENT_DELETED
from comcatlib.messages import NO_SUCH_ATTACHMENT
from comcatlib.messages import NO_SUCH_DAMAGE_REPORT
from damage_report import Attachment, DamageReport
from wsgilib import JSONMessage

from comcat.app.user_files import get_user_file


__all__ = ['ENDPOINTS']


def get_user_damage_reports() -> Iterable[UserDamageReport]:
    """Yields all damage reports of the user."""

    condition = UserDamageReport.user == USER.id
    return UserDamageReport.select().join(User).where(condition)


def get_user_damage_report(report_id: int) -> Iterable[UserDamageReport]:
    """Returns a damage report."""

    condition = UserDamageReport.id == report_id

    try:
        return get_user_damage_reports().where(condition).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT from None


def get_attachment(attachment_id: int) -> Attachment:
    """Returns the respective attachment."""

    select = Attachment.select().join(DamageReport).join(UserDamageReport)
    condition = UserDamageReport.user == USER.id
    condition &= Attachment.id == attachment_id

    try:
        return select.where(condition).get()
    except Attachment.DoesNotExist:
        raise NO_SUCH_ATTACHMENT from None


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Adds an attachment for the given damage report."""

    user_damage_report = get_user_damage_report(
        request.json.pop('userDamageReport'))
    user_file = get_user_file(request.json.pop('file'))
    attachment = Attachment(
        damage_report=user_damage_report.damage_report, file=user_file.file)
    attachment.save()
    return ATTACHMENT_ADDED.update(id=attachment.id)


@REQUIRE_OAUTH('comcat')
def delete(attachment_id: int) -> JSONMessage:
    """Removes the respective attachment."""

    attachment = get_attachment(attachment_id)
    attachment.delete_instance()
    return ATTACHMENT_DELETED


ENDPOINTS = (
    (['POST'], '/damage-report/attachment', post),
    (['DELETE'], '/damage-report/attachment/<int:attachment_id>', delete)
)
