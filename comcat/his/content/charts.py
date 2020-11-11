"""Management of charts assigned to ComCat accounts."""

from flask import request

from cmslib.functions.charts import get_chart
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from comcatlib import User, UserBaseChart
from his import CUSTOMER, authenticated, authorized
from mdb import Tenement
from wsgilib import JSON


__all__ = ['ROUTES']


def list_ubc(user=None):
    """Yields the user's base charts of the
    current customer for the respective user.
    """

    condition = Tenement.customer == CUSTOMER.id
    condition &= BaseChart.trashed == 0

    if user is not None:
        condition &= User.id == user

    return UserBaseChart.select().join(User).join(Tenement).switch(
        UserBaseChart).join(BaseChart).where(condition)


def get_ubc(ident):
    """Returns a UserBaseChart by its id and customer context."""

    return list_ubc().where(UserBaseChart.id == ident).get()


@authenticated
@authorized('comcat')
def get(ident):
    """Returns the respective UserBaseChart."""

    return JSON(get_ubc(ident).to_json(chart=True))


@authenticated
@authorized('comcat')
def list_(user):
    """Returns a list of UserBaseCharts of the given user."""

    return JSON([ubc.to_json(chart=True) for ubc in list_ubc(user)])


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


@authenticated
@authorized('comcat')
def chart_user_base_charts(ident):
    """Returns a list of UserBaseChart for the given chart."""

    chart = get_chart(ident)
    user_base_charts = UserBaseChart.select().where(
        UserBaseChart.base_chart == chart.base)
    users_base_charts = [ubc.to_json() for ubc in user_base_charts]
    return JSON(users_base_charts)


ROUTES = (
    ('GET', '/content/user/base-chart/<int:ident>', get),
    ('GET', '/content/user/<int:user>/base-chart', list_),
    ('POST', '/content/user/base-chart', add),
    ('PATCH', '/content/user/base-chart/<int:ident>', patch),
    ('DELETE', '/content/user/base-chart/<int:ident>', delete),
    ('GET', '/content/user/user-base-charts/<int:ident>',
     chart_user_base_charts)
)
