"""ComCat application backend."""

from datetime import timedelta
from json import load
from pathlib import Path

from flask import session

from comcatlib import init_app
from wsgilib import Application

from comcat.app.errors import ERRORS


__all__ = ['APPLICATION', 'RECAPTCHA_KEYS']


CORS = {
    'origins': [
        'http://localhost:4200',
        'capacitor://localhost:4200',
        'https://testing.homeinfo.de',
        'https://webapphi.web.app'
    ]
}
APPLICATION = Application('comcat', cors=CORS)
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['OAUTH2_TOKEN_EXPIRES_IN'] = {
    'authorization_code': timedelta(days=90).total_seconds()
}
APPLICATION.config['DEBUG'] = True
APPLICATION.config['TESTING'] = True
KEYFILE = Path('/usr/local/etc/comcat.secret')
RECAPTCHA = Path('/usr/local/etc/comcat.recaptcha')
RECAPTCHA_KEYS = {}


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""


    with KEYFILE.open('r') as keyfile:
        APPLICATION.secret_key = keyfile.read().strip()

    with RECAPTCHA.open('r') as recaptcha:
        RECAPTCHA_KEYS.update(load(recaptcha))

    init_app(APPLICATION)
    session.clear()


for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
