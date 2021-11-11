"""Damage report attachment endpoints."""

from contextlib import suppress

from flask import request

from comcatlib import ADDRESS
from comcatlib import CUSTOMER
from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import UserDamageReport
from damage_report import DamageReport, email
from wsgilib import JSON, JSONMessage

from comcat.app.functions import get_damage_reports, get_damage_report


__all__ = ['ROUTES']


DENIED_FIELDS = {'address', 'annotation', 'timestamp', 'checked'}


def jsonify(damage_report: DamageReport) -> dict:
    """JSONifys a damage report."""

    json = damage_report.to_json(attachments=True)

    with suppress(AttributeError):
        json['user'] = damage_report.userdamagereport.id

    return json


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Returns a list of sent damage report."""

    return JSON([jsonify(report) for report in get_damage_reports()])


@REQUIRE_OAUTH('comcat')
def get(report_id: int) -> JSON:
    """Returns a damage report."""

    return JSON(jsonify(get_damage_report(report_id)))


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


ROUTES = (
    (['GET'], '/damage-report', list_),
    (['GET'], '/damage-report/<int:report_id>', get),
    (['POST'], '/damage-report', post),
    (['DELETE'], '/damage-report/<int:report_id>', delete)
)
