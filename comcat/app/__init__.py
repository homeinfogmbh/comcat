"""Smartphone app endpoints."""

from comcat.app import damage_report
from comcat.app import file
from comcat.app import local_news
from comcat.app import lpt
from comcat.app import presentation
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = (
    damage_report.ENDPOINTS + file.ENDPOINTS + local_news.ENDPOINTS
    + lpt.ENDPOINTS + presentation.ENDPOINTS
)


for methods, path, function in ENDPOINTS:
    APPLICATION.route(path, methods=methods)(function)
