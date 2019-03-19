"""Management of menus assigned to ComCat accounts."""

from cmslib.functions.menu import get_menu
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from comcatlib import AccountMenu
from his import authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_account


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def get(acc_id):
    """Returns a list of IDs of the menus in the respective account."""

    return JSON([
        account_menu.menu.id for account_menu in AccountMenu.select().where(
            AccountMenu.account == get_account(acc_id))])


@authenticated
@authorized('comcat')
def add(acc_id, ident):
    """Adds the menu to the respective account."""

    account = get_account(acc_id)
    menu = get_menu(ident)

    try:
        AccountMenu.get(
            (AccountMenu.account == account) & (AccountMenu.menu == menu))
    except AccountMenu.DoesNotExist:
        account_menu = AccountMenu()
        account_menu.account = account
        account_menu.menu = menu
        account_menu.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('comcat')
def delete(acc_id, ident):
    """Deletes the menu from the respective account."""

    account = get_account(acc_id)
    menu = get_menu(ident)

    try:
        account_menu = AccountMenu.get(
            (AccountMenu.account == account) & (AccountMenu.menu == menu))
    except AccountMenu.DoesNotExist:
        raise NO_SUCH_CONTENT

    account_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/account/<int:acc_id>/menu', get, 'list_account_menus'),
    ('POST', '/content/account/<int:acc_id>/menu/<int:ident>', add,
     'add_account_menu'),
    ('DELETE', '/content/account/<int:acc_id>/menu/<int:ident>', delete,
     'delete_account_menu'))
