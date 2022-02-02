"""Comcat messenger."""

from flask import request

from ccmessenger import get_customer_messages
from ccmessenger import get_user_messages
from ccmessenger import UserMessage
from comcatlib import REQUIRE_OAUTH, CUSTOMER, USER
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def sent_messages() -> JSON:
    """Lists messages sent by the current user."""

    return JSON([
        message.to_json() for message in get_user_messages(sender=USER.id)
    ])


@REQUIRE_OAUTH('comcat')
def received_messages() -> JSON:
    """Lists messages sent to the current user."""

    return JSON([
        message.to_json() for message in get_customer_messages(
            recipient=USER.id
        )
    ])


@REQUIRE_OAUTH('comcat')
def send_message() -> JSONMessage:
    """Sends a new message."""

    message = UserMessage(
        sender=USER.id, recipient=CUSTOMER.id, text=request.json['text']
    )
    message.save()
    return JSONMessage('Message sent.', id=message.id, status=201)


ROUTES = [
    (['GET'], '/messenger/sent', sent_messages),
    (['GET'], '/messenger/received', received_messages),
    (['POST'], '/messenger/send', send_message)
]
