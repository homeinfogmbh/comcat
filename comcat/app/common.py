"""ComCat application backend."""

from typing import Union

from flask import Flask, session

from comcatlib import UserExpired, UserLocked, init_app
from comcatlib.messages.user import USER_EXPIRED, USER_LOCKED
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['OAUTH2_TOKEN_EXPIRES_IN'] = {'authorization_code': 86400}
APPLICATION.config['DEBUG'] = True
APPLICATION.config['TESTING'] = True

with open('/usr/local/etc/comcat.secret', 'r') as keyfile:
    APPLICATION.secret_key = keyfile.read().strip()


Message = Union[Response, JSONMessage]


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    init_app(APPLICATION)
    session.clear()


@APPLICATION.errorhandler(Response)
@APPLICATION.errorhandler(JSONMessage)
def errorhandler(message: Message) -> Message:
    """Returns the respective message."""

    return message


@APPLICATION.errorhandler(UserExpired)
def user_expired(_) -> JSONMessage:
    """Handles expired user account."""

    return USER_EXPIRED


@APPLICATION.errorhandler(UserLocked)
def user_locked(_) -> JSONMessage:
    """Handles locked user account."""

    return USER_LOCKED
