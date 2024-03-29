"""User logout."""

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH, logout
from wsgilib import JSONMessage


__all__ = ["ROUTES"]


@REQUIRE_OAUTH("comcat")
def logout_() -> JSONMessage:
    """Removes all tokens of a user."""

    logout(current_token.user)
    return JSONMessage("Tokens deleted.", status=200)


ROUTES = [(["DELETE"], "/logout", logout_)]
