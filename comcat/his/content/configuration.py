"""Management of configurations assigned to ComCat accounts."""

from typing import Iterable

from flask import request

from comcatlib import User, UserConfiguration
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


def list_user_configs(user: int) -> Iterable[UserConfiguration]:
    """Lists configuration assignments of the given user."""

    return UserConfiguration.select().join(User).where(
        (User.id == user) & (User.customer == CUSTOMER.id))


def get_user_config(ident: int) -> UserConfiguration:
    """Returns the given user configuration
    by its ID and customer context.
    """

    return UserConfiguration.select().join(User).where(
        (UserConfiguration.id == ident) & (User.customer == CUSTOMER.id)
    ).get()


@authenticated
@authorized('comcat')
def get(ident: int) -> JSON:
    """Returns the given UserConfiguration."""

    return JSON(get_user_config(ident).to_json())


@authenticated
@authorized('comcat')
def list_(user: int) -> JSON:
    """Returns a list of UserConfigurations of the given user."""

    return JSON([user_conf.to_json() for user_conf in list_user_configs(user)])


@authenticated
@authorized('comcat')
def add() -> JSONMessage:
    """Adds the configuration to the respective user."""

    user_configuration = UserConfiguration.from_json(request.json)
    user_configuration.save()
    return JSONMessage('User configuration added.', id=user_configuration.id,
                       status=201)


@authenticated
@authorized('comcat')
def delete(ident: int) -> JSONMessage:
    """Deletes the configuration from the respective user."""

    user_configuration = get_user_config(ident)
    user_configuration.delete_instance()
    return JSONMessage('User configuration deleted.', id=user_configuration.id,
                       status=200)


ROUTES = (
    ('GET', '/content/user/configuration/<int:ident>', get),
    ('GET', '/content/user/<int:user>/configuration', list_),
    ('POST', '/content/user/configuration', add),
    ('DELETE', '/content/user/configuration/<int:ident>', delete)
)
