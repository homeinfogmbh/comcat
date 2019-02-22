"""HIS management backend."""

from his import Application

from comcat.his import account, content


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
APPLICATION.add_routes(account.ROUTES + content.ROUTES)
