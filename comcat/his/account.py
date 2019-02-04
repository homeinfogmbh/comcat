"""Management of ComCat accounts."""

from functools import wraps

from flask import request

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.presentation.comcat_account import Presentation
from comcatlib import Account
from comcatlib.messages import ACCOUNT_ADDED
from comcatlib.messages import ACCOUNT_DELETED
from comcatlib.messages import ACCOUNT_PATCHED
from comcatlib.messages import NO_SUCH_ACCOUNT
from his import CUSTOMER, authenticated, authorized, admin
from wsgilib import JSON, XML


__all__ = ['ROUTES']


def get_accounts():
    """Yields ComCat accounts of the current customer."""

    return Account.select().where(Account.customer == CUSTOMER.id)


def get_account(ident):
    """Returns the respective ComCat account of the current customer."""

    try:
        return Account.get(
            (Account.id == ident) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT


def with_account(function):
    """Decorator to run the respective function
    with an account as first argument.
    """

    @wraps(function)
    def wrapper(ident, *args, **kwargs):
        """Wraps the original function."""
        return function(get_account(ident), *args, **kwargs)

    return wrapper


@authenticated
@authorized('comcat')
def list_():
    """Lists ComCat accounts."""

    return JSON([account.to_json() for account in get_accounts()])


@authenticated
@authorized('comcat')
@with_account
def get(account):
    """Lists ComCat accounts."""

    return JSON(account.to_json())


@authenticated
@authorized('comcat')
@admin
def add():
    """Adds a new ComCat account."""

    account = Account.from_json(request.json)
    account.save()
    return ACCOUNT_ADDED.update(account.id)


@authenticated
@authorized('comcat')
@admin
@with_account
def patch(account):
    """Updates the respective account."""

    account.patch_json(request.json)
    account.save()
    return ACCOUNT_PATCHED


@authenticated
@authorized('comcat')
@admin
@with_account
def delete(account):
    """Updates the respective account."""

    account.delete_instance()
    return ACCOUNT_DELETED


@authenticated
@authorized('comcat')
@with_account
def get_presentation(account):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(account)

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_json())

    try:
        presentation_dom = presentation.to_dom()
    except AmbiguousConfigurationsError:
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


ROUTES = (
    ('GET', '/comcat_account', list_, 'list_comcat_accounts'),
    ('GET', '/comcat_account/<int:ident>', get, 'get_comcat_account'),
    ('POST', '/comcat_account', add, 'add_comcat_account'),
    ('PATCH', '/comcat_account/<int:ident>', patch, 'patch_comcat_account'),
    ('DELETE', '/comcat_account/<int:ident>', delete, 'delete_comcat_account'),
    ('GET', '/comcat_account/<int:ident>/presentation', get_presentation,
     'get_comcat_account_presentation'))
