"""Smartphone app endpoints."""

from itertools import chain

from comcat.app import charts
from comcat.app import damage_report
from comcat.app import errors
from comcat.app import local_news
from comcat.app import logout
from comcat.app import lpt
from comcat.app import marketplace
from comcat.app import meta
from comcat.app import registration
from comcat.app import related_files
from comcat.app import tenant2tenant
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ENDPOINTS = [
    *charts.ENDPOINTS,
    *damage_report.ENDPOINTS,
    *local_news.ENDPOINTS,
    *logout.ENDPOINTS,
    *lpt.ENDPOINTS,
    *marketplace.ENDPOINTS,
    *meta.ENDPOINTS,
    *registration.ENDPOINTS,
    *related_files.ENDPOINTS,
    *tenant2tenant.ENDPOINTS
]
ERRORS = {
    **errors.ERRORS,
    **damage_report.ERRORS,
    **local_news.ERRORS,
    **related_files.ERRORS
}


for methods, path, function, name in ENDPOINTS:
    APPLICATION.add_url_rule(path, name, function, methods=methods)


for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
