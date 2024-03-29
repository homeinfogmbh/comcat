"""ComCat app interface for charts."""

from typing import Iterator

from peewee import JOIN, ModelSelect

from cmslib import BaseChart, Group, Groups, GroupBaseChart
from wsgilib import JSON

from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import UserBaseChart
from comcatlib import GroupMemberUser
from comcatlib import MenuBaseChart


__all__ = ["ROUTES", "get_base_charts"]


def user_groups() -> Iterator[Group]:
    """Yields all groups the given deployment is a member of."""

    groups = Group.select(cascade=True).where(
        Group.customer == USER.tenement.customer_id
    )

    for gmu in GroupMemberUser.select(cascade=True).where(
        GroupMemberUser.user == USER.id
    ):
        yield from Groups(groups).lineage(gmu.group)


def get_base_charts() -> ModelSelect:
    """Yields base charts, the current user has access to."""

    condition = UserBaseChart.user == USER.id
    condition |= GroupBaseChart.group << set(user_groups())
    condition &= BaseChart.trashed == 0

    return (
        BaseChart.select(cascade=True)
        .join_from(BaseChart, UserBaseChart, join_type=JOIN.LEFT_OUTER)
        .join_from(BaseChart, GroupBaseChart, join_type=JOIN.LEFT_OUTER)
        .where(condition)
    )


def get_menus(base_chart: BaseChart) -> ModelSelect:
    """Yields the menus for the base chart."""

    return MenuBaseChart.select(cascade=True).where(
        MenuBaseChart.base_chart == base_chart
    )


def jsonify_base_chart(base_chart: BaseChart) -> dict:
    """Returns a JSON-ish representation of the base chart."""

    json = base_chart.chart.to_json(skip={"schedule"})
    json["base"]["menus"] = [menu.menu.value for menu in get_menus(base_chart)]

    for user_base_chart in base_chart.userbasechart_set:
        json["index"] = user_base_chart.index

    for group_base_chart in base_chart.groupbasechart_set:
        json["index"] = group_base_chart.index

    return json


@REQUIRE_OAUTH("comcat")
def list_() -> JSON:
    """Lists available charts."""

    return JSON([jsonify_base_chart(bc) for bc in get_base_charts()])


ROUTES = [(["GET"], "/charts", list_)]
