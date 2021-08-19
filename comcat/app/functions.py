"""Damage-report related functions."""

from contextlib import suppress
from typing import Optional

from peewee import ModelSelect

from comcatlib import USER, UserDamageReport
from damage_report import Attachment, DamageReport
from tenant2tenant import TenantMessage


__all__ = [
    'get_attachment',
    'get_damage_report',
    'get_damage_reports',
    'get_user_damage_report',
    'get_user_damage_reports',
    'is_own_message',
    'get_sender_name'
]


def get_attachment(ident: int) -> Attachment:
    """Returns the respective attachment."""

    condition = UserDamageReport.user == USER.id
    condition &= Attachment.id == ident
    return Attachment.select().join(DamageReport).join(UserDamageReport).where(
        condition).get()


def get_damage_reports() -> ModelSelect:
    """Yields damage reports for the current user."""

    return DamageReport.select(cascade=True).join_from(
        DamageReport, UserDamageReport).where(UserDamageReport.user == USER.id)


def get_damage_report(ident: int) -> DamageReport:
    """Returns a damage report with the given ID."""

    return get_damage_reports().where(UserDamageReport.id == ident).get()


def get_user_damage_reports() -> ModelSelect:
    """Yields all damage reports of the user."""

    return UserDamageReport.select(cascade=True).where(
        UserDamageReport.user == USER.id)


def get_user_damage_report(ident: int) -> UserDamageReport:
    """Returns a damage report."""

    return get_user_damage_reports().where(UserDamageReport.id == ident).get()


def is_own_message(message: TenantMessage) -> bool:
    """Determines whether the tenant message is of the current user."""

    try:
        return message.usertenantmessage.user_id == USER.id
    except AttributeError:
        return False


def get_sender_name(message: TenantMessage) -> Optional[str]:
    """Returns the sender name if available."""

    try:
        return message.usertenantmessage.user.name
    except AttributeError:
        return None
