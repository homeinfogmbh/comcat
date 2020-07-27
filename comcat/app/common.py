"""ComCat application backend."""

from flask import Flask, session
from flask_cors import CORS

from comcatlib import init_app
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
CORS(APPLICATION, supports_credentials=True)
init_app(APPLICATION)
APPLICATION.secret_key = '/usr/local/etc/comcat.secret'
APPLICATION.config['SESSION_TYPE'] = 'filesystem'


@APPLICATION.before_first_request
def init():
    """Initializes the app."""

    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def handle_raised_message(message):
    """Returns the respective message."""

    return message
