"""HIS management backend."""

from his import Application

from comcat.his import account, address, content


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
APPLICATION.add_routes(account.ROUTES + address.ROUTES + content.ROUTES)
