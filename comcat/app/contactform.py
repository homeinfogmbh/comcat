"""Contact form."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, send_contact_mails
from wsgilib import JSONMessage


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def send() -> JSONMessage:
    """Sends a contact mail."""

    send_contact_mails(USER, request.json)
    return JSONMessage('Email sent.', status=200)


ROUTES = [(['POST'], '/contactform', send)]
