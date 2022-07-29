"""Meta backend."""

from io import BytesIO
from urllib.parse import urlencode

from authlib.integrations.flask_oauth2 import current_token
from flask import request
from qrcode import make
from wsgilib import Binary, JSON

from comcatlib import REQUIRE_OAUTH, USER, genpw


__all__ = ['ROUTES']


URL = 'de.homeinfo.comcat://register/{uid}/{passwd}'


def get_url() -> str:
    """Returns the respective URL."""

    user = current_token.user
    user.passwd = passwd = genpw()
    user.save()
    return URL.format(uid=user.id, passwd=urlencode(passwd))


@REQUIRE_OAUTH('comcat')
def get_qr_code() -> Binary:
    """Returns a QR code of the user's initialization nonce."""

    with BytesIO() as buf:
        make(get_url()).save(buf, format=request.args.get('format', 'png'))
        return Binary(buf.read())


@REQUIRE_OAUTH('comcat')
def user_info() -> JSON:
    """Returns the user information."""

    return JSON({
        'id': USER.id,
        'tenement': USER.tenement.id,
        'customer': USER.tenement.customer_id
    })


ROUTES = [
    (['GET'], '/init/qrcode', get_qr_code),
    (['GET'], '/user', user_info)
]
