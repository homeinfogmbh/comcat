"""Management of configurations assigned to ComCat accounts."""

from flask import request

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import NO_SUCH_CONTENT
from comcatlib import User, UserConfiguration
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def list_user_configs(user):
    """Lists configuration assignments of the given user."""

    return UserConfiguration.select().join(User).where(
        (User.id == user) & (User.customer == CUSTOMER.id))


def get_user_config(ident):
    """Returns the given user configuration
    by its ID and customer context.
    """

    return UserConfiguration.select().join(User).where(
        (UserConfiguration.id == ident) & (User.customer == CUSTOMER.id)
    ).get()


@authenticated
@authorized('comcat')
def get(ident):
    """Returns the given UserConfiguration."""

    return JSON(get_user_config(ident).to_json())


@authenticated
@authorized('comcat')
def list_(user):
    """Returns a list of UserConfigurations of the given user."""

    return JSON([user_conf.to_json() for user_conf in list_user_configs(user)])


@authenticated
@authorized('comcat')
def add():
    """Adds the configuration to the respective user."""

    user_configuration = UserConfiguration.from_json(request.json)
    user_configuration.save()
    return CONTENT_ADDED.update(id=user_configuration.id)


@authenticated
@authorized('comcat')
def delete(ident):
    """Deletes the configuration from the respective user."""

    try:
        user_configuration = get_user_config(ident)
    except UserConfiguration.DoesNotExist:
        raise NO_SUCH_CONTENT

    user_configuration.delete_instance()
    return CONTENT_DELETED.update(id=user_configuration.id)


ROUTES = (
    ('GET', '/content/user/configuration/<int:ident>', get),
    ('GET', '/content/user/<int:user>/configuration', list_),
    ('POST', '/content/user/configuration', add),
    ('DELETE', '/content/user/configuration/<int:ident>', delete)
)
