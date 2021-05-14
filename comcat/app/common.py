"""ComCat application backend."""

from datetime import timedelta

from flask import session

from comcatlib import init_app
from wsgilib import Application

from comcat.app.errors import ERRORS


__all__ = ['APPLICATION']


CORS = {
    'origins': [
        'http://localhost:4200',
        'https://testing.homeinfo.de',
        'https://webapphi.web.app'
    ]
}
APPLICATION = Application('comcat')
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['OAUTH2_TOKEN_EXPIRES_IN'] = {
    'authorization_code': timedelta(days=90).total_seconds()
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
