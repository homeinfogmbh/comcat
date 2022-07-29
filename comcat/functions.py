"""Damage-report related functions."""

from peewee import ModelSelect

from comcatlib import USER, User, UserDamageReport
from damage_report import Attachment, DamageReport
from mdb import Customer


__all__ = [
    'get_attachment',
    'get_comcat_customer',
    'get_damage_report',
    'get_damage_reports',
    'get_user_by_email',
    'get_user_damage_report',
    'get_user_damage_reports'
]


def get_attachment(ident: int) -> Attachment:
    """Returns the respective attachment."""

    condition = UserDamageReport.user == USER.id
    condition &= Attachment.id == ident
    return Attachment.select().join(DamageReport).join(UserDamageReport).where(
        condition).get()


def get_comcat_customer(ident: int) -> Customer:
    """Returns a customer instance of a valid ComCat customer."""

    return Customer.select(cascade=True).where(Customer.id == ident).get()


def get_damage_reports() -> ModelSelect:
    """Yields damage reports for the current user."""

    return DamageReport.select(UserDamageReport.user, cascade=True).join_from(
        DamageReport, UserDamageReport).where(UserDamageReport.user == USER.id)


def get_damage_report(ident: int) -> DamageReport:
    """Returns a damage report with the given ID."""

    return get_damage_reports().where(UserDamageReport.id == ident).get()


def get_user_by_email(email: str) -> User:
    """Returns a user by its email address."""

    return User.select(cascade=True).where(User.email == email).get()


def get_user_damage_reports() -> ModelSelect:
    """Yields all damage reports of the user."""

    return UserDamageReport.select(cascade=True).where(
        UserDamageReport.user == USER.id)


def get_user_damage_report(ident: int) -> UserDamageReport:
    """Returns a damage report."""

    return get_user_damage_reports().where(UserDamageReport.id == ident).get()
