"""Presentation endpoint."""

from hashlib import sha256
from json import dumps

from authlib.integrations.flask_oauth2 import current_token
from flask import request

from comcatlib import REQUIRE_OAUTH
from comcatlib import Presentation
from wsgilib import JSON


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def get_presentation():
    """Returns the presentation for the respective account."""

    presentation = Presentation(current_token.user)
    json = presentation.to_json()
    sha256sum = sha256(dumps(json).encode()).hexdigest()

    if sha256sum == request.headers.get('sha256sum'):
        return ('Not Modified', 304)

    json['sha256sum'] = sha256sum
    return JSON(json)


ENDPOINTS = ()  # TODO: implement.
