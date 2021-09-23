"""Damage report endpoints."""

from comcat.app.damage_report import attachment, damage_report


__all__ = ['ENDPOINTS', 'ERRORS']


ENDPOINTS = (*attachment.ENDPOINTS, *damage_report.ENDPOINTS)
ERRORS = {**attachment.ERRORS, **damage_report.ERRORS}
