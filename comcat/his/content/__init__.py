"""Content handling of ComCat accounts."""

from comcat.his.content import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = sum((configuration.ROUTES, menu.ROUTES), start=charts.ROUTES)
