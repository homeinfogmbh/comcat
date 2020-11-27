"""ComCat app interface for charts."""

from contextlib import suppress
from typing import Generator, Iterable

from peewee import JOIN

from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH, USER
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.group import Group, GroupMemberUser
from comcatlib.orm.menu import BaseChartMenu


__all__ = ['ENDPOINTS']


def user_groups() -> Generator[Group, None, None]:
    """Yields all groups the given deployment is a member of."""

    condition = GroupMemberUser.user == USER.id

    for gmu in GroupMemberUser.select().where(condition):
        yield gmu.group
        yield from gmu.group.parents


def get_user_base_charts() -> Iterable[BaseChart]:
    """Yields base charts, the current user has access to."""

    condition = UserBaseChart.user == USER.id
    condition |= GroupBaseChart.group << set(user_groups())
    condition &= BaseChart.trashed == 0     # Exclude trashed charts.
    return BaseChart.select().join(UserBaseChart, JOIN.LEFT_OUTER).join_from(
        BaseChart, GroupBaseChart, JOIN.LEFT_OUTER).where(condition)


def get_menus(base_chart: BaseChart) -> Iterable[BaseChartMenu]:
    """Yields the menus for the base chart."""

    return BaseChartMenu.select().where(BaseChartMenu.base_chart == base_chart)


def jsonify_base_chart(base_chart: BaseChart) -> dict:
    """Returns a JSON-ish representation of the base chart."""

    json = base_chart.chart.to_json()
    json['base']['menus'] = [menu.menu.value for menu in get_menus(base_chart)]

    with suppress(KeyError):    # Remove unneeded schedules.
        del json['base']['schedule']

    return json


@REQUIRE_OAUTH('comcat')
def list_() -> JSON:
    """Lists available charts."""

    return JSON([jsonify_base_chart(bc) for bc in get_user_base_charts()])


ENDPOINTS = ((['GET'], '/charts', list_),)
