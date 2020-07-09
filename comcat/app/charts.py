"""ComCat app interface for charts."""

from authlib.integrations.flask_oauth2 import current_token
from peewee import JOIN

from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.group import GroupMemberUser


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
    return BaseChart.select().join(UserBaseChart, JOIN.LEFT_OUTER).switch(
        BaseChart).join(GroupBaseChart, JOIN.LEFT_OUTER).where(condition)


def get_base_chart(ident):
    """Returns a base chart."""

    return get_user_base_charts().where(BaseChart.id == ident).get()


@REQUIRE_OAUTH('comcat')
def list_():
    """Lists available charts."""

    return JSON([bc.chart.to_json() for bc in get_user_base_charts()])


@REQUIRE_OAUTH('comcat')
def get(ident):
    """Returns a chart by it's base chart ID."""

    return JSON(get_base_chart(ident).chart.to_json())


ENDPOINTS = (
    (['GET'], '/charts', list_),
    (['GET'], '/chart/<int:ident>', get)
)
