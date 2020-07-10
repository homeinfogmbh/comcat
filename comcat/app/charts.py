"""ComCat app interface for charts."""

from contextlib import suppress

from authlib.integrations.flask_oauth2 import current_token
from peewee import JOIN

from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.group import GroupMemberUser
from comcatlib.orm.menu import BaseChartMenu


__all__ = ['ENDPOINTS']


def user_groups(user):
    """Yields all groups the given deployment is a member of."""

    condition = GroupMemberUser.user == user

    for gmu in GroupMemberUser.select().where(condition):
        yield gmu.group
        yield from gmu.group.parents


def get_user_base_charts():
    """Yields base charts, the current user has access to."""

    condition = UserBaseChart.user == current_token.user
    condition |= GroupBaseChart.group << set(user_groups(current_token.user))
    condition &= BaseChart.trashed == 0     # Exclude trashed charts.
    return BaseChart.select().join(UserBaseChart, JOIN.LEFT_OUTER).switch(
        BaseChart).join(GroupBaseChart, JOIN.LEFT_OUTER).where(condition)


def get_menus(base_chart):
    """Yields the menus for the base chart."""

    return BaseChartMenu.select().where(BaseChartMenu.base_chart == base_chart)


def jsonify_base_chart(base_chart):
    """Returns a JSON-ish representation of the base chart."""

    json = base_chart.chart.to_json()
    json['base']['menus'] = [menu.menu.value for menu in get_menus(base_chart)]

    with suppress(KeyError):    # Remove unneeded schedules.
        del json['base']['schedule']

    return json


@REQUIRE_OAUTH('comcat')
def list_():
    """Lists available charts."""

    return JSON([jsonify_base_chart(bc) for bc in get_user_base_charts()])


ENDPOINTS = ((['GET'], '/charts', list_),)
