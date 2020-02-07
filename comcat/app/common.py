"""ComCat application backend."""

from flask import Flask
from flask_cors import CORS

from comcatlib import init_oauth, init_oauth_endpoints
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION', 'DOMAIN']


APPLICATION = Flask('comcat')
CORS(APPLICATION, supports_credentials=True)
DOMAIN = 'wohninfo.homeinfo.de'
init_oauth(APPLICATION)
init_oauth_endpoints(APPLICATION)


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def handle_raised_message(message):
    """Returns the respective message."""

    return message
