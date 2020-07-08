"""Smartphone app endpoints."""

from comcat.app import charts
from comcat.app import damage_report
from comcat.app import file
from comcat.app import local_news
from comcat.app import lpt
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = sum(
    (damage_report.ENDPOINTS, file.ENDPOINTS, local_news.ENDPOINTS,
     lpt.ENDPOINTS),
    charts.ENDPOINTS
)


for methods, path, function in ENDPOINTS:
    APPLICATION.route(path, methods=methods)(function)
