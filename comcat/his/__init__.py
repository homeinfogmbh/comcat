"""HIS management backend."""

from his import Application

from comcat.his import account, address, content, group, tenement


__all__ = ['APPLICATION']


ROUTES = sum(
    (account.ROUTES, address.ROUTES, content.ROUTES, group.ROUTES,
     tenement.ROUTES),
    start=()
)
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
