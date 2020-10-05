"""Damage report endpoints."""

from flask import request

from comcatlib import ADDRESS
from comcatlib import CUSTOMER
from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import User
from comcatlib import UserDamageReport
from comcatlib.messages import ATTACHMENT_ADDED
from comcatlib.messages import ATTACHMENT_DELETED
from comcatlib.messages import DAMAGE_REPORT_ALREADY_PROCESSED
from comcatlib.messages import DAMAGE_REPORT_DELETED
from comcatlib.messages import DAMAGE_REPORT_SUBMITTED
from comcatlib.messages import NO_SUCH_ATTACHMENT
from comcatlib.messages import NO_SUCH_DAMAGE_REPORT
from damage_report import Attachment, DamageReport
from wsgilib import JSON

from comcat.app.user_files import get_user_file


__all__ = ['ENDPOINTS']


DENIED_FIELDS = {'address', 'timestamp', 'checked'}


def _get_user_damage_reports():
    """Yields all damage reports of the user."""

    condition = UserDamageReport.user == USER.id
    return UserDamageReport.select().join(User).where(condition)


def _get_user_damage_report(report_id):
    """Returns a damage report."""

    condition = UserDamageReport.id == report_id

    try:
        return _get_user_damage_reports().where(condition).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT from None


def _get_damage_reports():
    """Yields damage reports for the current user."""

    condition = UserDamageReport.user == USER.id
    return DamageReport.select().join(UserDamageReport).where(condition)


def _get_damage_report(report_id):
    """Returns a damage report with the given ID."""

    condition = UserDamageReport.id == report_id

    try:
        return _get_damage_reports().where(condition).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT from None


def _get_attachment(attachment_id):
    """Returns the respective attachment."""

    select = Attachment.select().join(DamageReport).join(UserDamageReport)
    condition = UserDamageReport.user == USER.id
    condition &= Attachment.id == attachment_id

    try:
        return select.where(condition).get()
    except Attachment.DoesNotExist:
        raise NO_SUCH_ATTACHMENT from None


@REQUIRE_OAUTH('comcat')
def list_damage_reports():
    """Returns a list of sent damage report."""

    return JSON([
        report.to_json(attachments=True) for report in _get_damage_reports()])


@REQUIRE_OAUTH('comcat')
def get_damage_report(report_id):
    """Returns a damage report."""

    return JSON(_get_damage_report(report_id).to_json(attachments=True))


@REQUIRE_OAUTH('comcat')
def submit_damage_report():
    """Submits a new damage report."""

    damage_report = DamageReport.from_json(
        request.json, CUSTOMER.id, ADDRESS.id, skip=DENIED_FIELDS)
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=USER.id, damage_report=damage_report)
    user_damage_report.save()
    return DAMAGE_REPORT_SUBMITTED.update(id=user_damage_report.id)


@REQUIRE_OAUTH('comcat')
def delete_damage_report(report_id):
    """Deletes the given damage report."""

    damage_report = _get_damage_report(report_id)

    if not damage_report.checked:
        # Deletion of corresponding damage report will also
        # delete user-damage report via database cascading.
        damage_report.delete_instance()
        return DAMAGE_REPORT_DELETED

    return DAMAGE_REPORT_ALREADY_PROCESSED


@REQUIRE_OAUTH('comcat')
def add_attachment():
    """Adds an attachment for the given damage report."""

    user_damage_report = _get_user_damage_report(
        request.json.pop('userDamageReport'))
    user_file = get_user_file(request.json.pop('file'))
    attachment = Attachment(
        damage_report=user_damage_report.damage_report, file=user_file.file)
    attachment.save()
    return ATTACHMENT_ADDED.update(id=attachment.id)


@REQUIRE_OAUTH('comcat')
def delete_attachment(attachment_id):
    """Removes the respective attachment."""

    attachment = _get_attachment(attachment_id)
    attachment.delete_instance()
    return ATTACHMENT_DELETED


ENDPOINTS = (
    (['GET'], '/damage-report', list_damage_reports),
    (['GET'], '/damage-report/<int:report_id>', get_damage_report),
    (['POST'], '/damage-report', submit_damage_report),
    (['DELETE'], '/damage-report/<int:report_id>', delete_damage_report),
    (['POST'], '/damage-report/attachment', add_attachment),
    (['DELETE'], '/damage-report/attachment/<int:attachment_id>',
     delete_attachment),
)
