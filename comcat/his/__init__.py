"""HIS management backend."""

from his import Application

from comcat.his import account, address, content, group, tenement


__all__ = ['APPLICATION']


ROUTES = sum(
    (address.ROUTES, content.ROUTES, group.ROUTES, tenement.ROUTES),
    account.ROUTES
)
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
