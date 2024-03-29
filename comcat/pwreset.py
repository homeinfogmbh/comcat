"""Password reset."""

from uuid import UUID

from flask import request

from comcatlib import NonceUsed
from comcatlib import PasswordResetPending
from comcatlib import get_config
from comcatlib import PasswordResetNonce
from comcatlib import User
from comcatlib import genpw
from comcatlib import send_new_password
from comcatlib import send_password_reset_email
from mtcaptcha import mtcaptcha
from wsgilib import JSONMessage

from comcat.functions import get_user_by_email


__all__ = ["ROUTES"]


PASSWORD_RESET_SENT = JSONMessage("Password reset sent.", status=200)


@mtcaptcha(
    lambda: request.json.pop("response"),
    lambda: get_config().get("mtcaptcha", "private_key"),
)
def request_pw_reset() -> JSONMessage:
    """Request a password reset."""

    try:
        user = get_user_by_email(request.json["email"])
    except (KeyError, TypeError):
        return JSONMessage("No email address specified.", status=400)
    except User.DoesNotExist:
        return PASSWORD_RESET_SENT  # Mitigate email sniffing.

    try:
        nonce = PasswordResetNonce.generate(user)
    except PasswordResetPending:
        return JSONMessage("A password reset is already pending.", status=403)

    nonce.save()
    send_password_reset_email(nonce)
    return PASSWORD_RESET_SENT


def confirm_pw_reset() -> JSONMessage:
    """Confirm a password reset."""

    try:
        nonce = UUID(request.json["nonce"])
    except (KeyError, TypeError):
        return JSONMessage("No nonce provided.", status=400)
    except ValueError:
        return JSONMessage("Invalid UUID provided.", status=400)

    try:
        nonce = PasswordResetNonce.use(nonce)
    except NonceUsed:
        return JSONMessage("Invalid nonce.", status=400)

    nonce.user.passwd = passwd = genpw()
    nonce.user.save()
    send_new_password(nonce.user, passwd)
    return JSONMessage("New password sent.")


ROUTES = [
    (["POST"], "/pwreset/request", request_pw_reset),
    (["POST"], "/pwreset/confirm", confirm_pw_reset),
]
