"""Damage report attachment endpoints."""

from typing import Iterable

from flask import request

from comcatlib import ADDRESS
from comcatlib import CUSTOMER
from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import UserDamageReport
from comcatlib.messages import DAMAGE_REPORT_ALREADY_PROCESSED
from comcatlib.messages import DAMAGE_REPORT_DELETED
from comcatlib.messages import DAMAGE_REPORT_SUBMITTED
from comcatlib.messages import NO_SUCH_DAMAGE_REPORT
from damage_report import DamageReport
from wsgilib import JSON, JSONMessage


__all__ = ['ENDPOINTS']


DENIED_FIELDS = {'address', 'timestamp', 'checked'}


def get_damage_reports() -> Iterable[UserDamageReport]:
    """Yields damage reports for the current user."""

    condition = UserDamageReport.user == USER.id
    return DamageReport.select().join(UserDamageReport).where(condition)


def get_damage_report(report_id: int) -> UserDamageReport:
    """Returns a damage report with the given ID."""

    condition = UserDamageReport.id == report_id

    try:
        return get_damage_reports().where(condition).get()
    except DamageReport.DoesNotExist:
        raise NO_SUCH_DAMAGE_REPORT from None


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
    return DAMAGE_REPORT_SUBMITTED.update(id=user_damage_report.id)


@REQUIRE_OAUTH('comcat')
def delete(report_id: int) -> JSONMessage:
    """Deletes the given damage report."""

    damage_report = get_damage_report(report_id)

    if not damage_report.checked:
        # Deletion of corresponding damage report will also
        # delete user-damage report via database cascading.
        damage_report.delete_instance()
        return DAMAGE_REPORT_DELETED

    return DAMAGE_REPORT_ALREADY_PROCESSED


ENDPOINTS = (
    (['GET'], '/damage-report', list_, 'list_damage_reports'),
    (['GET'], '/damage-report/<int:report_id>', get, 'get_damage_report'),
    (['POST'], '/damage-report', post, 'add_damage_report'),
    (['DELETE'], '/damage-report/<int:report_id>', delete,
     'delete_damage_report')
)
