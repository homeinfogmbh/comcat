"""Base chart menu assignment handling."""

from flask import request

from cmslib.orm.charts import BaseChart
from comcatlib.orm import BaseChartMenu
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


BASE_CHART_MENU_ADDED = JSONMessage('Base chart menu added.', 201)
NO_SUCH_BASE_CHART_MENU = JSONMessage('No such base chart menu.', 404)
BASE_CHART_MENU_DELETED = JSONMessage('Base chart menu deleted.', 200)


def get_base_chart_menus(base_chart_id):
    """Yields base chart menus for the given base chart."""

    condition = BaseChart.id == base_chart_id
    condition &= BaseChart.customer == CUSTOMER.id
    return BaseChartMenu.select().join(BaseChart).where(condition)


def get_base_chart_menu(base_chart_menu_id):
    """Returns the respective base chart menu."""

    condition = BaseChartMenu.id == base_chart_menu_id
    condition &= BaseChart.customer == CUSTOMER.id
    return BaseChartMenu.select().join(BaseChart).where(condition).get()


@authenticated
@authorized('comcat')
def list_(base_chart_id):
    """Lists menus of the respective base chart."""

    base_chart_menus = get_base_chart_menus(base_chart_id)
    return JSON([menu.to_json() for menu in base_chart_menus])


@authenticated
@authorized('comcat')
def add():
    """Adds a base chart menu."""

    base_chart_menu = BaseChartMenu.from_json(request.json)
    base_chart_menu.save()
    return BASE_CHART_MENU_ADDED.update(id=base_chart_menu.id)


@authenticated
@authorized('comcat')
def delete(ident):
    """Removes the base chart menu with the given ID."""

    try:
        base_chart_menu = get_base_chart_menu(ident)
    except BaseChartMenu.DoesNotExist:
        return NO_SUCH_BASE_CHART_MENU

    base_chart_menu.delete_instance()
    return BASE_CHART_MENU_DELETED


ROUTES = (
    ('GET', '/menu/<int:base_chart_id>', list_),
    ('POST', '/menu', add),
    ('DELETE', '/menu/<int:ident>', delete)
)
