"""Firebase Cloud Messaging."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, FCMToken, delete_tokens
from wsgilib import JSONMessage


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def add_token() -> JSONMessage:
    """Adds a new FCM token for the current user."""

    token = FCMToken(user=USER.id, token=request.json['token'])
    token.save()
    return JSONMessage('Token added.', id=token.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete_token(token: str) -> JSONMessage:
    """Deletes an FCM token for the current user."""

    delete_tokens(USER.id, token)
    return JSONMessage('Token deleted.', status=200)


ROUTES = [
    (['POST'], '/fcm', add_token),
    (['DELETE'], '/fcm/<token>', delete_token),
]
