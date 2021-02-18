"""Damage-report related functions."""

from functools import wraps
from typing import Any, Callable

from flask import request
from peewee import ModelSelect

from comcatlib import USER, UserDamageReport, UserFile
from damage_report import Attachment, DamageReport


__all__ = [
    'get_attachment',
    'get_damage_report',
    'get_damage_reports',
    'get_user_damage_report',
    'get_user_damage_reports',
    'get_user_file',
    'with_user_file'
]


def get_attachment(ident: int) -> Attachment:
    """Returns the respective attachment."""

    condition = UserDamageReport.user == USER.id
    condition &= Attachment.id == ident
    return Attachment.select().join(UserDamageReport).where(condition).get()


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


def get_user_file(ident: int, *, direct: bool = False) -> UserFile:
    """Returns the user file with the given ID."""

    condition = UserFile.user == USER.id

    if direct:
        condition &= UserFile.file == ident
    else:
        condition &= UserFile.id == ident

    return UserFile.select(cascade=True).where(condition).get()


def with_user_file(function: Callable[..., Any]) -> Callable[..., Any]:
    """Returns the respective user file."""

    @wraps(function)
    def wrapper(ident: int, *args, **kwargs):
        """Wraps the decorated function."""
        direct = request.args.get('direct', False)
        return function(get_user_file(ident, direct=direct), *args, **kwargs)

    return wrapper
