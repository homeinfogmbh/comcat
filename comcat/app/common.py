"""ComCat application backend."""

from flask import Flask, session

from comcatlib import REQUIRE_OAUTH
from comcatlib import USER
from comcatlib import UserExpired
from comcatlib import UserLocked
from comcatlib import init_app
from comcatlib import InitializationNonce
from comcatlib.messages.user import USER_EXPIRED, USER_LOCKED
from wsgilib import JSONMessage, Response


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
APPLICATION.config['SESSION_TYPE'] = 'filesystem'

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


@REQUIRE_OAUTH('comcat')
def generate_initialization_nonce():
    """Generates a new initialization nonce."""

    try:
        nonce = InitializationNonce.get(InitializationNonce.user == USER.id)
    except InitializationNonce.DoesNotExist:
        nonce = InitializationNonce.add(user=USER.id)

    return nonce.uuid.hex
