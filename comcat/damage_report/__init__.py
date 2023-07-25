"""Damage report endpoints."""

from damage_report import ERRORS

from comcat.damage_report import attachment, damage_report


__all__ = ["ROUTES", "ERRORS"]


ROUTES = [*attachment.ROUTES, *damage_report.ROUTES]
