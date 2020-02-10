"""Management of configurations assigned to ComCat accounts."""

from cmslib.functions.configuration import get_configuration
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from comcatlib import User, UserConfiguration
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_user


__all__ = ['ROUTES']


def list_user_configs(user):
    """Lists configurations of the given user."""

    return UserConfiguration.select().join(User).where(
        (User.id == user) & (User.customer == CUSTOMER.id))


@authenticated
@authorized('comcat')
def get(user):
    """Returns a list of IDs of the configurations
    of the given user.
    """

    return JSON([
        user_configuration.configuration.id for user_configuration
        in list_user_configs(user)])


@authenticated
@authorized('comcat')
def add(user, ident):
    """Adds the configuration to the respective user."""

    user = get_user(user)
    configuration = get_configuration(ident)

    try:
        UserConfiguration.get(
            (UserConfiguration.user == user)
            & (UserConfiguration.configuration == configuration))
    except UserConfiguration.DoesNotExist:
        user_configuration = UserConfiguration()
        user_configuration.user = user
        user_configuration.configuration = configuration
        user_configuration.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('comcat')
def delete(user, ident):
    """Deletes the configuration from the respective user."""

    user = get_user(user)
    configuration = get_configuration(ident)

    try:
        user_configuration = UserConfiguration.get(
            (UserConfiguration.user == user)
            & (UserConfiguration.configuration == configuration))
    except UserConfiguration.DoesNotExist:
        raise NO_SUCH_CONTENT

    user_configuration.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/account/<int:user>/configuration', get),
    ('POST', '/content/account/<int:user>/configuration/<int:ident>', add),
    ('DELETE', '/content/account/<int:user>/configuration/<int:ident>',
     delete)
)
