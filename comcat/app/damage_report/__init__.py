"""Damage report endpoints."""

from damage_report import ERRORS

from comcat.app.damage_report import attachment, damage_report


__all__ = ['ENDPOINTS', 'ERRORS']


ENDPOINTS = (*attachment.ENDPOINTS, *damage_report.ENDPOINTS)
