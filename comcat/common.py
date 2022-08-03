"""ComCat application backend."""

from datetime import timedelta
from json import load

from flask import session

from comcatlib import init_oauth_endpoints
from wsgilib import Application


__all__ = ['APPLICATION']


with open('/usr/local/etc/comcat.d/cors.json', 'r') as cors:
    CORS = load(cors)

APPLICATION = Application('comcat', cors=CORS, debug=True)
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


@APPLICATION.before_first_request
def before_first_request():
    """Initializes the app."""

    init_oauth_endpoints(APPLICATION)
    session.clear()
