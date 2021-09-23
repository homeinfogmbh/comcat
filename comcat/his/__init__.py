"""HIS management backend."""

from his import Application

from comcat.his import content
from comcat.his import damage_report
from comcat.his import group
from comcat.his import marketplace
from comcat.his import menu
from comcat.his import tenant2tenant
from comcat.his import tenement
from comcat.his import user
from comcat.his import errors


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
ROUTES = (
    *content.ROUTES,
    *damage_report.ROUTES,
    *group.ROUTES,
    *marketplace.ROUTES,
    *menu.ROUTES,
    *tenant2tenant.ROUTES,
    *tenement.ROUTES,
    *user.ROUTES
)
ERRORS = {**errors.ERRORS, **marketplace.ERRORS}


APPLICATION.add_routes(ROUTES)
APPLICATION.register_error_handlers(ERRORS)
