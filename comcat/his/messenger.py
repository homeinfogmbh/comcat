"""Comcat messenger."""

from flask import request

from ccmessenger import get_customer_messages
from ccmessenger import get_user_messages
from ccmessenger import CustomerMessage
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage

from comcat.his.functions import get_user


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def sent_messages() -> JSON:
    """Lists sent messages."""

    return JSON([
        message.to_json() for message in get_customer_messages(
            sender=CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def received_messages() -> JSON:
    """Lists received messages."""

    return JSON([
        message.to_json() for message in get_user_messages(
            recipient=CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def show_conversation(user: int) -> JSON:
    """Shows the conversation with a user."""

    return JSON([
        message.to_json() for message in get_user_messages(
            sender=user, recipient=CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def send_message() -> JSONMessage:
    """Write a new message."""

    message = CustomerMessage(
        sender=CUSTOMER.id,
        recipient=get_user(request.json.get('user')),
        text=request.json['text']
    )
    message.save()
    return JSONMessage('Message sent.', id=message.id, status=201)


ROUTES = [
    (['GET'], '/messenger/sent', sent_messages),
    (['GET'], '/messenger/received', received_messages),
    (['GET'], '/messenger/conversation/<int:user>', show_conversation),
    (['POST'], '/messenger/send', send_message)
]
