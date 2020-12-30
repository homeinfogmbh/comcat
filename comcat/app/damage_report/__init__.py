"""Damage report endpoints."""

from comcat.app.damage_report import attachment, damage_report


__all__ = ['ENDPOINTS']


ENDPOINTS = (*attachment.ENDPOINTS, *damage_report.ENDPOINTS)
