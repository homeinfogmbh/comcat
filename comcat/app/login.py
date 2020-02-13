"""ComCat login procedure."""

from uuid import UUID

from flask import request

from comcatlib import get_session_duration
from comcatlib import User
from comcatlib import Session
from comcatlib.messages import INVALID_CREDENTIALS
from wsgilib import JSON


__all__ = ['login']


def login():
    """Logs in an end user."""

    print('Raw data:', request.data, flush=True)
    uuid = request.form.get('uuid')
    passwd = request.form.get('passwd')

    print('UUID:', uuid, 'passwd:', passwd, flush=True)
    from json import dumps
    print('Form:', dumps(request.form, indent=2), flush=True)

    if not uuid or not passwd:
        return INVALID_CREDENTIALS

    try:
        uuid = UUID(uuid)
    except (ValueError, TypeError):
        return INVALID_CREDENTIALS

    try:
        user = User.get(User.uuid == uuid)
    except User.DoesNotExist:
        return INVALID_CREDENTIALS  # Mitigate user sniffing.

    if user.login(passwd):
        session = Session.open(user, duration=get_session_duration())
        response = JSON(session.to_json())
        session_token = session.token.hex   # pylint: disable=E1101
        response.set_cookie('session', session_token, expires=session.end)
        return response

    return INVALID_CREDENTIALS
