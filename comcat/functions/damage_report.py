"""Functions to handle damage reports."""

from flask import request

from comcatlib import ACCOUNT, AccountDamageReport
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from damage_report import DamageReport


__all__ = ['get_damage_reports', 'submit_damage_report']


def get_damage_reports():
    """Yields damage reports."""

    return DamageReport.select().join(AccountDamageReport).where(
        AccountDamageReport.account == ACCOUNT.id)


def submit_damage_report():
    """Submits a damage report."""

    address = ACCOUNT.address

    if address is None:
        raise NO_ADDRESS_CONFIGURED

    damage_report = DamageReport.from_json(
        request.json, ACCOUNT.customer, address)
    damage_report.save()
    account_damage_report = AccountDamageReport(
        id=ACCOUNT.id, damage_report=damage_report)
    account_damage_report.save()
