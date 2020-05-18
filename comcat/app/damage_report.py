"""Damage report endpoints."""

from authlib.integrations.flask_oauth2 import current_token
from flask import request

from comcatlib import REQUIRE_OAUTH, User, UserDamageReport
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from damage_report import DamageReport, Attachment
from wsgilib import JSON, JSONMessage


__all__ = [
    'list_damage_reports',
    'get_damage_report',
    'submit_damage_report',
    'get_attachment'
]


DENIED_FIELDS = {'address', 'timestamp', 'checked'}

DAMAGE_REPORT_SUBMITTED = JSONMessage('Damage report submitted.', status=201)
NO_SUCH_ATTACHMENT = JSONMessage('No such attachment.', status=404)
NO_SUCH_DAMAGE_REPORT = JSONMessage('No such damage report.', status=404)


def _get_damage_reports():
    """Yields all damage reports of the user."""

    select = DamageReport.select().join(UserDamageReport).join(User)
    condition_owner = UserDamageReport.submitter == current_token.user
    condition_other = UserDamageReport.submitter != current_token.user
    condition_other &= UserDamageReport.private == 0
    condition_other &= User.tenement == current_token.user.tenement
    condition = condition_owner | condition_other
    return select.where(condition)


def _get_damage_report(report_id):
    """Returns a damage report."""

    try:
        return _get_damage_reports().where(DamageReport.id == report_id).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT


def _get_attachment(report_id, attachment_id):
    """Returns the respective attachment."""

    select = Attachment.select().join(DamageReport).join(UserDamageReport)
    condition = Attachment.id == attachment_id
    condition &= DamageReport.id == report_id
    condition &= UserDamageReport.user == current_token.user

    try:
        return select.where(condition).get()
    except Attachment.DoesNotExist:
        raise NO_SUCH_ATTACHMENT


@REQUIRE_OAUTH('comcat')
def list_damage_reports():
    """Returns a list of sent damage report."""

    damage_reports = _get_damage_reports()
    return JSON([report.to_dict() for report in damage_reports])


@REQUIRE_OAUTH('comcat')
def get_damage_report(report_id):
    """Returns a damage report."""

    damage_report = _get_damage_report(report_id)
    return JSON(damage_report.to_json())


@REQUIRE_OAUTH('comcat')
def submit_damage_report():
    """Submits a new damage report."""

    address = current_token.user.address

    if address is None:
        raise NO_ADDRESS_CONFIGURED

    damage_report = DamageReport.from_json(
        request.json, current_token.user.customer, address, skip=DENIED_FIELDS
    )
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=current_token.user, damage_report=damage_report
    )
    user_damage_report.save()
    return DAMAGE_REPORT_SUBMITTED


@REQUIRE_OAUTH('comcat')
def get_attachment(report_id, attachment_id):
    """Returns an image from the damage report."""

    attachment = _get_attachment(report_id, attachment_id)
    return attachment.bytes
