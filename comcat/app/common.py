"""ComCat application backend."""

from datetime import timedelta
from json import load
from pathlib import Path

from flask import session

from comcatlib import init_app
from wsgilib import Application

from comcat.app import errors
from comcat.app import damage_report
from comcat.app import local_news


__all__ = ['APPLICATION', 'RECAPTCHA_KEYS']


with open('/usr/local/etc/comcat.d/cors.json', 'r') as cors:
    CORS = load(cors)

APPLICATION = Application('comcat', cors=CORS)
APPLICATION.config['SESSION_TYPE'] = 'filesystem'
APPLICATION.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True
APPLICATION.config['OAUTH2_TOKEN_EXPIRES_IN'] = {
    'authorization_code': timedelta(days=90).total_seconds()
}
APPLICATION.config['DEBUG'] = True
APPLICATION.config['TESTING'] = True

# Needs to be set before "APPLICATION.before_first_request" is run.
with open('/usr/local/etc/comcat.secret', 'r') as keyfile:
    APPLICATION.secret_key = keyfile.read().strip()

RECAPTCHA = Path('/usr/local/etc/comcat.recaptcha')
RECAPTCHA_KEYS = {}


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    with RECAPTCHA.open('r') as recaptcha:
        RECAPTCHA_KEYS.update(load(recaptcha))

    init_app(APPLICATION)
    session.clear()

ERRORS = {
    **errors.ERRORS,
    **damage_report.ERRORS,
    **local_news.ERRORS
}

for exception, handler in ERRORS.items():
    APPLICATION.register_error_handler(exception, handler)
