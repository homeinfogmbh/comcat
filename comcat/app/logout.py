"""User logout."""

from authlib.integrations.flask_oauth2 import current_token

from wsgilib import JSONMessage

from comcat.functions import logout


__all__ = ['ROUTES']


def logout_() -> JSONMessage:
    """Removes all tokens of a user."""

    logout(current_token.user)
    return JSONMessage('Tokens deleted.', status=200)


ROUTES = [(['DELETE'], '/logout', logout_, 'user_logout')]
