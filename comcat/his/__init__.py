"""HIS management backend."""

from his import Application

from comcat.his import address, content, group, tenement, user


__all__ = ['APPLICATION']


ROUTES = sum(
    (content.ROUTES, group.ROUTES, tenement.ROUTES, user.ROUTES),
    address.ROUTES
)
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
