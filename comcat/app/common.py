"""ComCat application backend."""

from flask import Flask, session

from comcatlib import UserExpired, UserLocked, init_app
from comcatlib.messages.user import USER_EXPIRED, USER_LOCKED
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['DEBUG'] = True
APPLICATION.config['TESTING'] = True

with open('/usr/local/etc/comcat.secret', 'r') as keyfile:
    APPLICATION.secret_key = keyfile.read().strip()


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    init_app(APPLICATION)
    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def errorhandler(message):
    """Returns the respective message."""

    return message


@APPLICATION.errorhandler(UserExpired)
def user_expired(_):
    """Handles expired user account."""

    return USER_EXPIRED


@APPLICATION.errorhandler(UserLocked)
def user_locked(_):
    """Handles locked user account."""

    return USER_LOCKED
