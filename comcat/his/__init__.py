"""HIS management backend."""

from his import Application

from comcat.his import content, group, menu, tenement, user


__all__ = ['APPLICATION']


ROUTES = [*content.ROUTES, *group.ROUTES, *menu.ROUTES, *tenement.ROUTES,
          *user.ROUTES]
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
