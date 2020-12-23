"""HIS management backend."""

from his import Application

from comcat.his import content, group, menu, tenement, user


__all__ = ['APPLICATION']


APPLICATION = Application('comcat')
APPLICATION.add_routes(content.ROUTES)
APPLICATION.add_routes(group.ROUTES)
APPLICATION.add_routes(menu.ROUTES)
APPLICATION.add_routes(tenement.ROUTES)
APPLICATION.add_routes(user.ROUTES)
