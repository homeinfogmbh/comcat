"""Damage report endpoints."""

from comcat.app.damage_report import attachment, damage_report
from comcat.app.damage_report.errors import ERRORS


__all__ = ['ENDPOINTS', 'ERRORS']


ENDPOINTS = (*attachment.ENDPOINTS, *damage_report.ENDPOINTS)
