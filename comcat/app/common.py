"""ComCat application backend."""

from flask import Flask, session
from flask_cors import CORS

from comcatlib import init_oauth, init_oauth_endpoints
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION', 'DOMAIN']


APPLICATION = Flask('comcat')
CORS(APPLICATION, supports_credentials=True)
DOMAIN = 'wohninfo.homeinfo.de'


def init_app(application):
    """Initializes the application."""

    application.secret_key = '/usr/local/etc/comcat.secret'
    application.config['SESSION_TYPE'] = 'filesystem'


init_oauth(APPLICATION)
init_oauth_endpoints(APPLICATION)
init_app(APPLICATION)


@APPLICATION.before_first_request
def init():
    """Initializes the app."""

    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def handle_raised_message(message):
    """Returns the respective message."""

    return message
