"""Management of charts assigned to ComCat accounts."""

from flask import request
from peewee import JOIN

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from comcatlib import User, UserBaseChart
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


USER_JOIN = UserBaseChart.user == User.id
BASE_CHART_JOIN = UserBaseChart.base_chart == BaseChart.id


def list_ubc(user=None):
    """Yields the user's base charts of the
    current customer for the respective user.
    """

    condition = User.customer == CUSTOMER.id

    if user is not None:
        condition &= User.id == user

    condition &= BaseChart.trashed == 0
    return UserBaseChart.select().join(
        User, join_type=JOIN.LEFT_OUTER, on=USER_JOIN
    ).join(
        BaseChart, join_type=JOIN.LEFT_OUTER, on=BASE_CHART_JOIN
    ).where(condition)


def get_ubc(ident):
    """Returns a UserBaseChart by its id and customer context."""

    return UserBaseChart.select().join(User).where(
        (UserBaseChart.id == ident) & (User.customer == CUSTOMER.id)
    ).get()


@authenticated
@authorized('comcat')
def mapping():
    """Returns a mapping of base-chart → user."""

    json = {}

    for ubc in list_ubc():
        json[ubc.base_chart_id] = ubc.user_id

    return JSON(json)


@authenticated
@authorized('comcat')
def get(ident):
    """Returns the respective UserBaseChart."""

    return JSON(get_ubc(ident).to_json())


@authenticated
@authorized('comcat')
def list_(user):
    """Returns a list of UserBaseCharts of the given user."""

    return JSON([ubc.to_json() for ubc in list_ubc(user)])


@authenticated
@authorized('comcat')
def add():
    """Adds the chart to the respective user."""

    user_base_chart = UserBaseChart.from_json(request.json)
    user_base_chart.save()
    return CONTENT_ADDED.update(id=user_base_chart.id)


@authenticated
@authorized('comcat')
def patch(ident):
    """Adds the chart to the respective user."""

    try:
        user_base_chart = get_ubc(ident)
    except UserBaseChart.DoesNotExist:
        return NO_SUCH_CONTENT

    user_base_chart.patch_json(request.json)
    user_base_chart.save()
    return CONTENT_PATCHED.update(id=user_base_chart.id)


@authenticated
@authorized('comcat')
def delete(ident):
    """Deletes the chart from the respective user."""

    try:
        user_base_chart = get_ubc(ident)
    except UserBaseChart.DoesNotExist:
        return NO_SUCH_CONTENT

    user_base_chart.delete_instance()
    return CONTENT_DELETED.update(id=user_base_chart.id)


ROUTES = (
    ('GET', '/content/user/base-chart', mapping),
    ('GET', '/content/user/base-chart/<int:ident>', get),
    ('GET', '/content/user/<int:user>/base-chart', list_),
    ('POST', '/content/user/base-chart', add),
    ('PATCH', '/content/user/base-chart/<int:ident>', patch),
    ('DELETE', '/content/user/base-chart/<int:ident>', delete)
)
