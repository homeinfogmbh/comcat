"""Firebase Cloud Messaging."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, FCMToken, delete_tokens
from wsgilib import JSONMessage


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def _add_token() -> JSONMessage:
    """Adds a new FCM token for the current user."""

    token = FCMToken(user=USER.id, token=request.json['token'])
    token.save()
    return JSONMessage('Token added.', status=201)


@REQUIRE_OAUTH('comcat')
def _delete_token(token: str) -> JSONMessage:
    """Deletes an FCM token for the current user."""

    delete_tokens(USER.id, token)
    return JSONMessage('Token deleted.', status=200)


ROUTES = [
    (['POST'], '/fcm', _add_token),
    (['DELETE'], '/fcm/<token>', _delete_token),
]
