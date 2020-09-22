"""ComCat application backend."""

from flask import Flask, session

from comcatlib import init_app
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    init_app(APPLICATION)
    APPLICATION.config['SESSION_TYPE'] = 'filesystem'

    with open('/usr/local/etc/comcat.secret', 'r') as keyfile:
        APPLICATION.secret_key = keyfile.read().strip()

    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def errorhandler(message):
    """Returns the respective message."""

    return message
