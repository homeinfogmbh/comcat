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
from comcat.app import tenantforum
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ROUTES = [
    *charts.ROUTES,
    *damage_report.ROUTES,
    *local_news.ROUTES,
    *logout.ROUTES,
    *lpt.ROUTES,
    *marketplace.ROUTES,
    *meta.ROUTES,
    *registration.ROUTES,
    *related_files.ROUTES,
    *tenant2tenant.ROUTES,
    *tenantforum.ROUTES
]
ERRORS = {
    **errors.ERRORS,
    **damage_report.ERRORS,
    **local_news.ERRORS,
    **marketplace.ERRORS,
    **related_files.ERRORS,
    **tenant2tenant.ERRORS
}


APPLICATION.add_routes(ROUTES)
APPLICATION.register_error_handlers(ERRORS)
