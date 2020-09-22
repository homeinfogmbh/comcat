"""ComCat application backend."""

from uuid import uuid4

from flask import Flask, session

from comcatlib import init_app
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
init_app(APPLICATION)
APPLICATION.secret_key = uuid4().bytes
APPLICATION.config['SESSION_TYPE'] = 'filesystem'


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def errorhandler(message):
    """Returns the respective message."""

    return message
