"""ComCat login."""

from flask import request

from his.messages import InvalidCredentials
from his.messages import MissingCredentials
from wsgilib import JSON

from comcat.orm import DEFAULT_SESSION_DURATION, Account, Session


__all__ = ['login']


def _get_duration():
    """Returns the repsective session duration in minutes."""

    return int(request.args.get('duration', DEFAULT_SESSION_DURATION))


def login():
    """Logs in an end user."""

    account = request.json.get('account')
    passwd = request.json.get('passwd')

    if not account or not passwd:
        return MissingCredentials()

    try:
        account = Account.get(Account.name == account)
    except Account.DoesNotExist:
        return InvalidCredentials()     # Mitigate account spoofing.

    if account.login(passwd):
        session = Session.open(account, duration=_get_duration())
        return JSON(session.to_json())

    return InvalidCredentials()
