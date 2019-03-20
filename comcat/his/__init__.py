"""HIS management backend."""

from his import Application

from comcat.his import account, address, content, group


__all__ = ['APPLICATION']


ROUTES = account.ROUTES + address.ROUTES + content.ROUTES + group.ROUTES
APPLICATION = Application('comcat')
APPLICATION.add_routes(ROUTES)
