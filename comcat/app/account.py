"""Account management."""

from uuid import UUID

from flask import request

from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import InvalidPassword
from comcatlib import confirm_email_change
from comcatlib import request_email_change
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


PATCH_FIELDS = {'phone', 'mobile'}


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


@REQUIRE_OAUTH('comcat')
def _request_email_change() -> JSONMessage:
    """Requests and email change."""

    request_email_change(USER, request.json['email'])
    return JSONMessage('Email change request issued.', status=201)


def _confirm_email_change() -> JSONMessage:
    """Confirms the email change."""

    try:
        uuid = UUID(request.json['uuid'])
    except (KeyError, TypeError):
        return JSONMessage('No UUID specified.', status=400)
    except ValueError:
        return JSONMessage('Invalid UUID specified.', status=400)

    if not (passwd := request.json.get('passwd')):
        return JSONMessage('No password specified.', status=400)

    confirm_email_change(uuid, passwd)
    return JSONMessage('Email address updated.', status=200)


ROUTES = [
    (['GET'], '/account', get_account_info),
    (['PATCH'], '/account', change_account_info),
    (['POST'], '/account/delete', delete_account),
    (['PATCH'], '/account/email', _request_email_change),
    (['PUT'], '/account/email', _confirm_email_change)
]
