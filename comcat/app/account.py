"""Account management."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, InvalidPassword
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


PATCH_FIELDS = frozenset()


@REQUIRE_OAUTH('comcat')
def get_account_info() -> JSON:
    """Returns the account information."""

    return JSON(USER.to_json(tenement=True))


@REQUIRE_OAUTH('comcat')
def change_account_info() -> JSONMessage:
    """Changes the account information."""

    user = USER.patch_json(request.json, only=PATCH_FIELDS)
    user.save()
    return JSONMessage('Account updated.', status=200)


@REQUIRE_OAUTH('comcat')
def delete_account() -> JSONMessage:
    """Deletes the account."""

    try:
        USER.delete_account(request.json.get('passwd'))
    except InvalidPassword:
        return JSONMessage('Invalid password.', status=400)

    return JSONMessage('Account deleted.', status=200)


ROUTES = [
    (['GET'], '/account', get_account_info),
    (['PATCH'], '/account', change_account_info),
    (['POST'], '/account/delete', delete_account)
]
