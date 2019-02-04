"""Content handling of ComCat accounts."""

from dscms4.content.comcat_account import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = charts.ROUTES + configuration.ROUTES + menu.ROUTES
