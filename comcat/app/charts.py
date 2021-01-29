"""ComCat app interface for charts."""

from typing import Iterator

from peewee import ModelSelect

from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.group import Group
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH, USER
from comcatlib import UserBaseChart
from comcatlib import GroupMemberUser
from comcatlib import MenuBaseChart


__all__ = ['ENDPOINTS', 'get_base_charts']


def user_groups() -> Iterator[Group]:
    """Yields all groups the given deployment is a member of."""

    condition = GroupMemberUser.user == USER.id

    for gmu in GroupMemberUser.select(cascade=True).where(condition):
        yield gmu.group
        yield from gmu.group.parents


def get_base_charts() -> ModelSelect:
    """Yields base charts, the current user has access to."""

    condition = UserBaseChart.user == USER.id
    condition |= GroupBaseChart.group << set(user_groups())
    condition &= BaseChart.trashed == 0

    return BaseChart.select(cascade=True).join_from(
        BaseChart, UserBaseChart).join_from(
        BaseChart, GroupBaseChart).where(condition)


def get_menus(base_chart: BaseChart) -> ModelSelect:
    """Yields the menus for the base chart."""

    return MenuBaseChart.select(cascade=True).where(
        MenuBaseChart.base_chart == base_chart)


def jsonify_base_chart(base_chart: BaseChart) -> dict:
    """Returns a JSON-ish representation of the base chart."""

    json = base_chart.chart.to_json(skip={'schedule'})
    json['base']['menus'] = [menu.menu.value for menu in get_menus(base_chart)]
    print('JSON-ifyed base chart:', json, flush=True)
    return json


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists available charts."""

    return JSON([jsonify_base_chart(bc) for bc in get_base_charts()])


ENDPOINTS = [(['GET'], '/charts', list_, 'list_charts')]
