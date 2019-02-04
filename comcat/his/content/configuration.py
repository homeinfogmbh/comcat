"""Management of configurations assigned to ComCat accounts."""

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from comcatlib import get_account, AccountConfiguration
from his import authenticated, authorized
from wsgilib import JSON

from dscms4.configuration import get_configuration


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def get(acc_id):
    """Returns a list of IDs of the configurations
    in the respective account.
    """

    return JSON([
        account_configuration.configuration.id for account_configuration
        in AccountConfiguration.select().where(
            AccountConfiguration.account == get_account(acc_id))])


@authenticated
@authorized('comcat')
def add(acc_id, ident):
    """Adds the configuration to the respective account."""

    account = get_account(acc_id)
    configuration = get_configuration(ident)

    try:
        AccountConfiguration.get(
            (AccountConfiguration.account == account)
            & (AccountConfiguration.configuration == configuration))
    except AccountConfiguration.DoesNotExist:
        account_configuration = AccountConfiguration()
        account_configuration.account = account
        account_configuration.configuration = configuration
        account_configuration.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('comcat')
def delete(acc_id, ident):
    """Deletes the configuration from the respective account."""

    account = get_account(acc_id)
    configuration = get_configuration(ident)

    try:
        account_configuration = AccountConfiguration.get(
            (AccountConfiguration.account == account)
            & (AccountConfiguration.configuration == configuration))
    except AccountConfiguration.DoesNotExist:
        raise NO_SUCH_CONTENT

    account_configuration.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/comcat_account/<int:acc_id>/configuration', get,
     'list_comcat_account_configurations'),
    ('POST', '/content/comcat_account/<int:acc_id>/configuration/<int:ident>',
     add, 'add_comcat_account_configuration'),
    ('DELETE',
     '/content/comcat_account/<int:acc_id>/configuration/<int:ident>',
     delete, 'delete_comcat_accountl_configuration'))
