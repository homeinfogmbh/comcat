"""HIS management backend."""

from his import Application

import ccmessenger

from comcat.his import contact_emails
from comcat.his import content
from comcat.his import damage_report
from comcat.his import group
from comcat.his import marketplace
from comcat.his import menu
from comcat.his import messenger
from comcat.his import registration
from comcat.his import tenantcalendar
from comcat.his import tenantforum
from comcat.his import tenement
from comcat.his import user
from comcat.his import errors


__all__ = ['APPLICATION']


APPLICATION = Application('comcat', debug=True)
ROUTES = (
    *contact_emails.ROUTES,
    *content.ROUTES,
    *damage_report.ROUTES,
    *group.ROUTES,
    *marketplace.ROUTES,
    *menu.ROUTES,
    *messenger.ROUTES,
    *registration.ROUTES,
    *tenantcalendar.ROUTES,
    *tenantforum.ROUTES,
    *tenement.ROUTES,
    *user.ROUTES
)
ERRORS = {
    **errors.ERRORS,
    **marketplace.ERRORS,
    **ccmessenger.ERRORS,
    **tenantcalendar.ERRORS,
    **tenantforum.ERRORS
}


APPLICATION.add_routes(ROUTES)
APPLICATION.register_error_handlers(ERRORS)
