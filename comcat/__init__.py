"""Smartphone app endpoints."""

import ccmessenger

from comcat import account
from comcat import charts
from comcat import contactform
from comcat import damage_report
from comcat import errors
from comcat import fcm
from comcat import local_news
from comcat import logout
from comcat import lpt
from comcat import marketplace
from comcat import messenger
from comcat import meta
from comcat import news
from comcat import pwreset
from comcat import registration
from comcat import related_files
from comcat import reporting
from comcat import tenantcalendar
from comcat import tenantforum
from comcat.common import APPLICATION


__all__ = ['APPLICATION']


ROUTES = [
    *account.ROUTES,
    *charts.ROUTES,
    *contactform.ROUTES,
    *damage_report.ROUTES,
    *fcm.ROUTES,
    *local_news.ROUTES,
    *logout.ROUTES,
    *lpt.ROUTES,
    *marketplace.ROUTES,
    *messenger.ROUTES,
    *meta.ROUTES,
    *news.ROUTES,
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
