"""HIS management backend."""

from his import Application

from comcat.his import content, damage_report, group, menu, tenement, user
from comcat.his.errors import ERRORS


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
ROUTES = (
    *content.ROUTES, *damage_report.ROUTES, *group.ROUTES, *menu.ROUTES,
    *tenement.ROUTES, *user.ROUTES
)
APPLICATION.add_routes(ROUTES)


for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
