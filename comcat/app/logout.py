"""User logout."""

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import Token
from wsgilib import JSONMessage


__all__ = ['ROUTES']


def logout() -> JSONMessage:
    """Removes all tokens of a user."""

    Token.delete().where(Token.user == current_token.user)
    return JSONMessage('Tokens deleted.', status=200)


ROUTES = [('DELETE', '/logout', logout)]
