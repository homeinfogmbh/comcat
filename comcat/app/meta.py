"""Meta backend."""

from io import BytesIO

from flask import request
from qrcode import make
from wsgilib import Bytes

from comcatlib import REQUIRE_OAUTH, USER, InitializationNonce


__all__ = ['ENDPOINTS']


def _get_nonce():
    """Returns an existing Nonce or creates a new one."""

    try:
        return InitializationNonce.get(InitializationNonce.user == USER.id)
    except InitializationNonce.DoesNotExist:
        return InitializationNonce.add(user=USER.id)


@REQUIRE_OAUTH('comcat')
def generate_initialization_nonce():
    """Generates a new initialization nonce."""

    return _get_nonce().uuid.hex


@REQUIRE_OAUTH('comcat')
def get_qr_code():
    """Returns a QR code of the user's initialization nonce."""

    format = request.args.get('format', 'png')  # pylint: disable=W0622
    qrcode = make(_get_nonce().url)

    with BytesIO() as buf:
        qrcode.save(buf, format=format)
        return Bytes(buf.read())


ENDPOINTS = [
    (['GET'], '/init/nonce', generate_initialization_nonce),
    (['GET'], '/init/qrcode', get_qr_code)
]
