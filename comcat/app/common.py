"""ComCat application backend."""

from flask import Flask, session

from comcatlib import init_app

from comcat.app.errors import ERRORS


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['OAUTH2_TOKEN_EXPIRES_IN'] = {
    'authorization_code': 30 * 24 * 60 * 60     # 30 days in seconds.
}
APPLICATION.config['DEBUG'] = True
APPLICATION.config['TESTING'] = True

with open('/usr/local/etc/comcat.secret', 'r') as keyfile:
    APPLICATION.secret_key = keyfile.read().strip()


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    init_app(APPLICATION)
    session.clear()


for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
