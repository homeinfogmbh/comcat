"""Smartphone app endpoints."""

import ccmessenger

from comcat.app import account
from comcat.app import charts
from comcat.app import contactform
from comcat.app import damage_report
from comcat.app import errors
from comcat.app import local_news
from comcat.app import logout
from comcat.app import lpt
from comcat.app import marketplace
from comcat.app import messenger
from comcat.app import meta
from comcat.app import pwreset
from comcat.app import registration
from comcat.app import related_files
from comcat.app import reporting
from comcat.app import tenantcalendar
from comcat.app import tenantforum
from comcat.app.common import APPLICATION


__all__ = ['APPLICATION']


ROUTES = [
    *account.ROUTES,
    *charts.ROUTES,
    *contactform.ROUTES,
    *damage_report.ROUTES,
    *local_news.ROUTES,
    *logout.ROUTES,
    *lpt.ROUTES,
    *marketplace.ROUTES,
    *messenger.ROUTES,
    *meta.ROUTES,
    *pwreset.ROUTES,
    *registration.ROUTES,
    *related_files.ROUTES,
    *reporting.ROUTES,
    *tenantcalendar.ROUTES,
    *tenantforum.ROUTES
]
ERRORS = {
    **errors.ERRORS,
    **damage_report.ERRORS,
    **local_news.ERRORS,
    **marketplace.ERRORS,
    **ccmessenger.ERRORS,
    **related_files.ERRORS,
    **tenantcalendar.ERRORS,
    **tenantforum.ERRORS
}


APPLICATION.add_routes(ROUTES)
APPLICATION.register_error_handlers(ERRORS)
