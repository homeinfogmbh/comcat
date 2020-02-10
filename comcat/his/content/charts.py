"""Management of charts assigned to ComCat accounts."""

from flask import request

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


def list_ubc(ident):
    """Yields the user's base charts of the
    current customer for the respective user.
    """

    return UserBaseChart.select().join(
        User, join_type='LEFT', on=USER_JOIN).join(
            BaseChart, join_type='LEFT', on=BASE_CHART_JOIN).where(
                (User.customer == CUSTOMER.id) & (User.id == ident)
                & (BaseChart.trashed == 0))


def get_ubc(user, base_chart):
    """Returns the respective account base chart."""

    return UserBaseChart.select().join(User).where(
        (User.customer == CUSTOMER.id) & (User.id == user)
        & (UserBaseChart.base_chart == base_chart)).get()


@authenticated
@authorized('comcat')
def get(user):
    """Returns a list of user base charts of the given user."""

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
def patch(user, base_chart):
    """Adds the chart to the respective user."""

    try:
        user_base_chart = get_ubc(user, base_chart)
    except UserBaseChart.DoesNotExist:
        return NO_SUCH_CONTENT

    user_base_chart.patch_json(request.json)
    user_base_chart.save()
    return CONTENT_PATCHED


@authenticated
@authorized('comcat')
def delete(user, base_chart):
    """Deletes the chart from the respective user."""

    try:
        user_base_chart = get_ubc(user, base_chart)
    except UserBaseChart.DoesNotExist:
        return NO_SUCH_CONTENT

    user_base_chart.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/user/<int:user>/chart', get),
    ('POST', '/content/user/chart', add),
    ('PATCH', '/content/user/<int:user>/chart/<int:base_chart>', patch),
    ('DELETE', '/content/user/<int:user>/chart/<int:base_chart>', delete)
)
