"""Content handling of ComCat accounts."""

from comcat.his.content import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = sum((charts.ROUTES, configuration.ROUTES, menu.ROUTES), start=())
