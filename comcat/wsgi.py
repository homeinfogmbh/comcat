"""ComCat login."""

from hashlib import sha256
from json import dumps

from flask import request

from cmslib.presentation.comcat_account import Presentation
from comcatlib import ACCOUNT
from comcatlib import Account
from comcatlib import Session
from comcatlib import authenticated
from comcatlib import get_session_duration
from comcatlib.messages import INVALID_CREDENTIALS
from wsgilib import JSON


__all__ = ['login']


def login():
    """Logs in an end user."""

    account = request.json.get('account')
    passwd = request.json.get('passwd')

    if not account or not passwd:
        return INVALID_CREDENTIALS

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return INVALID_CREDENTIALS  # Mitigate account spoofing.

    if account.login(passwd):
        session = Session.open(account, duration=get_session_duration())
        return JSON(session.to_json())

    return INVALID_CREDENTIALS


@authenticated
def get_presentation():
    """Returns the presentation for the respective account."""

    presentation = Presentation(ACCOUNT.id)
    json = presentation.to_json()
    sha256sum = sha256(dumps(json).encode()).hexdigest()

    if request.headers.get('sha256sum') == sha256sum:
        return ('Not Modified', 304)

    json['sha256sum'] = sha256sum
    return JSON(json)
