"""HIS management backend."""

from his import Application

from comcat.his import content, group, menu, user


__all__ = ['APPLICATION']


ROUTES = sum((content.ROUTES, group.ROUTES, menu.ROUTES), user.ROUTES)
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
