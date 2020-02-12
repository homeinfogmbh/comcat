"""Damage report endpoints."""

from authlib.integrations.flask_oauth2 import current_token
from flask import request

from comcatlib import REQUIRE_OAUTH
from comcatlib import UserDamageReport
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from damage_report import DamageReport
from wsgilib import JSON


__all__ = ['list_damage_reports', 'submit_damage_report']


DENIED_FIELDS = ('address', 'timestamp', 'checked')


@REQUIRE_OAUTH('comcat')
def list_damage_reports():
    """Returns a list of sent damage report."""

    select = UserDamageReport.user == current_token.user
    damage_reports = DamageReport.select().join(UserDamageReport).where(select)
    return JSON([damage_report.to_dict() for damage_report in damage_reports])


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
    return ('Damage report submitted.', 201)
