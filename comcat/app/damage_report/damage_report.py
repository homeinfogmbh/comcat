"""Damage report attachment endpoints."""

from flask import request

from comcatlib import ADDRESS
from comcatlib import CUSTOMER
from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import UserDamageReport
from damage_report import DamageReport, email
from wsgilib import JSON, JSONMessage

from comcat.app.functions import get_damage_reports, get_damage_report


__all__ = ['ENDPOINTS', 'ERRORS']


DENIED_FIELDS = {'address', 'annotation', 'timestamp', 'checked'}
ERRORS = {
    DamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such damage report.', status=404)
}


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Returns a list of sent damage report."""

    return JSON([
        report.to_json(attachments=True) for report in get_damage_reports()])


@REQUIRE_OAUTH('comcat')
def get(report_id: int) -> JSON:
    """Returns a damage report."""

    return JSON(get_damage_report(report_id).to_json(attachments=True))


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Submits a new damage report."""

    damage_report = DamageReport.from_json(
        request.json, CUSTOMER.id, ADDRESS.id, skip=DENIED_FIELDS)
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=USER.id, damage_report=damage_report)
    user_damage_report.save()
    email(damage_report)
    return JSONMessage(
        'Damage report submitted.', id=user_damage_report.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete(report_id: int) -> JSONMessage:
    """Deletes the given damage report."""

    damage_report = get_damage_report(report_id)

    if not damage_report.checked:
        # Deletion of corresponding damage report will also
        # delete user-damage report via database cascading.
        damage_report.delete_instance()
        return JSONMessage('Damage report deleted.', status=200)

    return JSONMessage('Damage report already processed.', status=403)


ENDPOINTS = (
    (['GET'], '/damage-report', list_, 'list_damage_reports'),
    (['GET'], '/damage-report/<int:report_id>', get, 'get_damage_report'),
    (['POST'], '/damage-report', post, 'add_damage_report'),
    (['DELETE'], '/damage-report/<int:report_id>', delete,
     'delete_damage_report')
)
