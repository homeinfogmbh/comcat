"""Smartphone app endpoints."""

from comcat.app import charts
from comcat.app import damage_report
from comcat.app import local_news
from comcat.app import lpt
from comcat.app import meta
from comcat.app import related_files
from comcat.app import tenant2tenant
from comcat.app import user_files
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = {
    'charts': charts.ENDPOINTS,
    'damage_report': damage_report.ENDPOINTS,
    'local_news': local_news.ENDPOINTS,
    'lpt': lpt.ENDPOINTS,
    'meta': meta.ENDPOINTS,
    'related_files': related_files.ENDPOINTS,
    'tenant2tenant': tenant2tenant.ENDPOINTS,
    'user_files': user_files.ENDPOINTS
}


for name, endpoints in ENDPOINTS.items():
    for methods, path, function in endpoints:
        APPLICATION.add_url_rule(path, f'{name}:{function}', function,
                                 methods=methods)
