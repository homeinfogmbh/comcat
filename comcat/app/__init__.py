"""Smartphone app endpoints."""

from comcat.app import charts
from comcat.app import damage_report
from comcat.app import local_news
from comcat.app import lpt
from comcat.app import user_files
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = sum(
    (damage_report.ENDPOINTS, local_news.ENDPOINTS, lpt.ENDPOINTS,
     user_files.ENDPOINTS),
    charts.ENDPOINTS
)


for methods, path, function in ENDPOINTS:
    APPLICATION.route(path, methods=methods)(function)
