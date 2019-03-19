"""Management of charts assigned to ComCat accounts."""

from flask import request

from cmslib.functions.charts import get_chart
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from comcatlib import Account, AccountBaseChart
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_account


__all__ = ['ROUTES']


def list_abc(ident):
    """Yields the account base charts of the
    current customer for the respective account.
    """

    term_join = AccountBaseChart.account == Account.id
    bc_join = AccountBaseChart.base_chart == BaseChart.id
    return AccountBaseChart.select().join(
        Account, join_type='LEFT', on=term_join).join(
            BaseChart, join_type='LEFT', on=bc_join).where(
                (Account.customer == CUSTOMER.id) & (Account.id == ident)
                & (BaseChart.trashed == 0))


def get_abc(acc_id, ident):
    """Returns the respective account base chart."""

    try:
        return AccountBaseChart.select().join(Account).where(
            (AccountBaseChart.id == ident)
            & (Account.customer == CUSTOMER.id)
            & (Account.id == acc_id)).get()
    except AccountBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


@authenticated
@authorized('comcat')
def get(acc_id):
    """Returns a list of IDs of the charts in the respective account."""

    return JSON([abc.to_json() for abc in list_abc(acc_id)])


@authenticated
@authorized('comcat')
def add(acc_id, ident):
    """Adds the chart to the respective account."""

    account = get_account(acc_id)
    base_chart = get_chart(ident).base
    account_base_chart = AccountBaseChart.from_json(
        request.json, account, base_chart)
    account_base_chart.save()
    return CONTENT_ADDED.update(id=account_base_chart.id)


@authenticated
@authorized('comcat')
def patch(acc_id, ident):
    """Adds the chart to the respective account."""

    account_base_chart = get_abc(acc_id, ident)
    account_base_chart.patch_json(request.json)
    account_base_chart.save()
    return CONTENT_PATCHED


@authenticated
@authorized('comcat')
def delete(acc_id, ident):
    """Deletes the chart from the respective account."""

    account_base_chart = get_abc(acc_id, ident)
    account_base_chart.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/account/<int:acc_id>/chart', get, 'list_account_charts'),
    ('POST', '/content/account/<int:acc_id>/chart/<int:ident>', add,
     'add_account_chart'),
    ('PATCH', '/content/account/<int:acc_id>/chart/<int:ident>', patch,
     'patch_account_chart'),
    ('DELETE', '/content/account/<int:acc_id>/chart/<int:ident>', delete,
     'delete_account_chart'))
