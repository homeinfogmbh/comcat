"""Password reset."""

from uuid import UUID

from flask import request

from comcatlib import NonceUsed
from comcatlib import PasswordResetPending
from comcatlib import get_config
from comcatlib import PasswordResetNonce
from comcatlib import User
from comcatlib import send_password_reset_email
from peeweeplus import PasswordTooShort
from recaptcha import recaptcha
from wsgilib import JSONMessage

from comcat.app.functions import get_user_by_email


__all__ = ['ROUTES']


PASSWORD_RESET_SENT = JSONMessage('Password reset sent.', status=200)


@recaptcha(get_config)
def request_pw_reset() -> JSONMessage:
    """Request a password reset."""

    try:
        user = get_user_by_email(request.json['email'])
    except (KeyError, TypeError):
        return JSONMessage('No email address specified.', status=400)
    except User.DoesNotExist:
        return PASSWORD_RESET_SENT  # Mitigate email sniffing.

    try:
        nonce = PasswordResetNonce.generate(user)
    except PasswordResetPending:
        return JSONMessage('A password reset is already pending.', status=403)

    nonce.save()
    send_password_reset_email(nonce)
    return PASSWORD_RESET_SENT


@recaptcha(get_config)
def confirm_pw_reset() -> JSONMessage:
    """Confirm a password reset."""

    try:
        uuid = UUID(request.json['nonce'])
    except (KeyError, TypeError):
        return JSONMessage('No nonce provided.', status=400)
    except ValueError:
        return JSONMessage('Invalid UUID provided.', status=400)

    try:
        nonce = PasswordResetNonce.use(uuid)
    except NonceUsed:
        return JSONMessage('Invalid nonce provided.', status=403)

    try:
        (user := nonce.user).passwd = request.json['passwd']
    except KeyError:
        return JSONMessage('No password provided.', status=400)
    except PasswordTooShort as error:
        return JSONMessage('Password too short.', min=error.minlen, status=400)

    user.save()
    return JSONMessage('Password reset.', status=200)


ROUTES = [
    ('POST', '/pwreset/request', request_pw_reset),
    ('POST', '/pwreset/confirm', confirm_pw_reset)
]
