"""Smartphone app endpoints."""

from comcat.app import charts
from comcat.app import damage_report
from comcat.app import local_news
from comcat.app import lpt
from comcat.app import related_files
from comcat.app import user_files
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = {
    'charts': charts.ENDPOINTS,
    'damage_report': damage_report.ENDPOINTS,
    'local_news': local_news.ENDPOINTS,
    'lpt': lpt.ENDPOINTS,
    'related_files': related_files.ENDPOINTS,
    'user_files': user_files.ENDPOINTS
}


for endpoint, (methods, path, function) in ENDPOINTS.items():
    APPLICATION.route(path, methods=methods, endpoint=endpoint)(function)
