"""Damage report endpoints."""

from authlib.integrations.flask_oauth2 import current_token
from flask import request

from comcatlib import oauth
from comcatlib import User
from comcatlib import UserDamageReport
from comcatlib import DamageReportAttachment
from comcatlib.messages import ATTACHMENT_ADDED
from comcatlib.messages import ATTACHMENT_DELETED
from comcatlib.messages import DAMAGE_REPORT_ALREADY_PROCESSED
from comcatlib.messages import DAMAGE_REPORT_DELETED
from comcatlib.messages import DAMAGE_REPORT_SUBMITTED
from comcatlib.messages import MISSING_ADDRESS
from comcatlib.messages import NO_SUCH_ATTACHMENT
from comcatlib.messages import NO_SUCH_DAMAGE_REPORT
from damage_report import DamageReport
from wsgilib import JSON

from comcat.app.user_files import get_file


__all__ = ['ENDPOINTS']


DENIED_FIELDS = {'address', 'timestamp', 'checked'}


def _get_damage_report_condition():
    """Damage report selection condition."""

    return UserDamageReport.user == current_token.user


def _get_user_damage_reports():
    """Yields all damage reports of the user."""

    condition = _get_damage_report_condition()
    return UserDamageReport.select().join(User).where(condition)


def _get_user_damage_report(report_id):
    """Returns a damage report."""

    condition = UserDamageReport.id == report_id

    try:
        return _get_user_damage_reports().where(condition).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT


def _get_damage_reports():
    """Yields damage reports for the current user."""

    condition = _get_damage_report_condition()
    select = DamageReport.select().join(UserDamageReport).join(User)
    return select.where(condition)


def _get_damage_report(report_id):
    """Returns a damage report with the given ID."""

    condition = _get_damage_report_condition()
    condition &= UserDamageReport.id == report_id

    try:
        return DamageReport.select().join(UserDamageReport).join(User).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT


def _get_attachments(report_id):
    """Returns the attachments of the given damage report."""

    select = DamageReportAttachment.select().join(UserDamageReport).join(User)
    condition = _get_damage_report_condition()
    condition &= UserDamageReport.damage_report == report_id
    return select.where(condition)


def _get_attachment(attachment_id):
    """Returns the respective attachment."""

    select = DamageReportAttachment.select().join(UserDamageReport).join(User)
    condition = _get_damage_report_condition()
    condition &= DamageReportAttachment.id == attachment_id

    try:
        return select.where(condition).get()
    except DamageReportAttachment.DoesNotExist:
        raise NO_SUCH_ATTACHMENT


@oauth('comcat')
def list_damage_reports():
    """Returns a list of sent damage report."""

    return JSON([report.to_json() for report in _get_damage_reports()])


@oauth('comcat')
def get_damage_report(report_id):
    """Returns a damage report."""

    return JSON(_get_damage_report(report_id).to_json())


@oauth('comcat')
def submit_damage_report():
    """Submits a new damage report."""

    address = current_token.user.tenement.address

    if address is None:
        raise MISSING_ADDRESS

    damage_report = DamageReport.from_json(
        request.json, current_token.user.customer, address,
        skip=DENIED_FIELDS)
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=current_token.user, damage_report=damage_report)
    user_damage_report.save()
    return DAMAGE_REPORT_SUBMITTED.update(id=user_damage_report.id)


@oauth('comcat')
def delete_damage_report(report_id):
    """Deletes the given damage report."""

    user_damage_report = _get_user_damage_report(report_id)
    damage_report = user_damage_report.damage_report

    if not damage_report.checked:
        # Deletion of corresponding damage report will also
        # delete user-damage report via database cascading.
        damage_report.delete_instance()
        return DAMAGE_REPORT_DELETED

    return DAMAGE_REPORT_ALREADY_PROCESSED


@oauth('comcat')
def list_attachments(report_id):
    """Returns a list of available attachments for the damage report."""

    return JSON([attachment.id for attachment in _get_attachments(report_id)])


@oauth('comcat')
def get_attachment(attachment_id):
    """Returns an image from the damage report."""

    attachment = _get_attachment(attachment_id)
    return JSON(attachment.to_json())


@oauth('comcat')
def submit_attachment():
    """Adds an attachment for the given damage report."""

    user_damage_report_id = request.json.pop('userDamageReport')
    file_id = request.json.pop('file')
    user_damage_report = _get_user_damage_report(user_damage_report_id)
    file = get_file(file_id)
    attachment = DamageReportAttachment(
        user_damage_report=user_damage_report, file=file)
    attachment.save()
    return ATTACHMENT_ADDED.update(id=attachment.id)


@oauth('comcat')
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
    (['GET'], '/damage-report/<int:report_id>/attachment', list_attachments),
    (['GET'], '/damage-report/attachment/<int:attachment_id>', get_attachment),
    (['POST'], '/damage-report/attachment', submit_attachment),
    (['DELETE'], '/damage-report/attachment/<int:attachment_id>',
     delete_attachment),
)
