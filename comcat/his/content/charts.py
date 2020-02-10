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


def list_ubc(ident):
    """Yields the user's base charts of the
    current customer for the respective user.
    """

    term_join = UserBaseChart.account == User.id
    bc_join = UserBaseChart.base_chart == BaseChart.id
    return UserBaseChart.select().join(
        User, join_type='LEFT', on=term_join).join(
            BaseChart, join_type='LEFT', on=bc_join).where(
                (User.customer == CUSTOMER.id) & (User.id == ident)
                & (BaseChart.trashed == 0))


def get_ubc(user, ident):
    """Returns the respective account base chart."""

    try:
        return UserBaseChart.select().join(User).where(
            (UserBaseChart.id == ident)
            & (User.customer == CUSTOMER.id)
            & (User.id == user)).get()
    except UserBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


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
def patch(user, ident):
    """Adds the chart to the respective user."""

    user_base_chart = get_ubc(user, ident)
    user_base_chart.patch_json(request.json)
    user_base_chart.save()
    return CONTENT_PATCHED


@authenticated
@authorized('comcat')
def delete(user, ident):
    """Deletes the chart from the respective user."""

    user_base_chart = get_ubc(user, ident)
    user_base_chart.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/user/<int:acc_id>/chart', get),
    ('POST', '/content/user/chart', add),
    ('PATCH', '/content/user/<int:acc_id>/chart/<int:ident>', patch),
    ('DELETE', '/content/user/<int:acc_id>/chart/<int:ident>', delete)
)
