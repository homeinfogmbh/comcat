"""Base chart menu assignment handling."""

from flask import request

from cmslib import get_base_chart
from comcatlib.orm.menu import Menu, MenuBaseChart
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage

from comcat.his.functions import get_menu_base_chart, get_menu_base_charts


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists menus of the respective base chart."""

    return JSON([mbc.to_json() for mbc in get_menu_base_charts(CUSTOMER.id)])


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Returns the menus of the respective base chart."""

    return JSON(get_menu_base_chart(ident, CUSTOMER.id).to_json())


@authenticated
@authorized('comcat')
def add() -> JSONMessage:
    """Adds a base chart menu."""

    base_chart = get_base_chart(request.json.pop('baseChart'), CUSTOMER.id)
    menu = Menu(request.json.pop('menu'))
    mbc = MenuBaseChart(base_chart=base_chart, menu=menu)
    mbc.save()
    return JSONMessage('Base chart menu added.', id=mbc.id, status=201)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Removes the base chart menu with the given ID."""

    get_menu_base_chart(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Base chart menu deleted.', status=200)


ROUTES = [
    ('GET', '/menu/base_chart', list_),
    ('GET', '/menu/base_chart/<int:ident>', get),
    ('POST', '/menu/base_chart', add),
    ('DELETE', '/menu/base_chart/<int:ident>', delete)
]
