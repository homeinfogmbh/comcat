"""Comcat messenger."""

from ccmessenger import get_customer_messages, get_user_messages
from wsgilib import JSON, JSONMessage

from comcat.his.functions import get_user


__all__ = ['ROUTES']


def list_messges() -> JSON:
    """Lists messages."""

    return JSON([message.to_json() for message in get_customer_messages(
        CUSTOMER.id)])


def show_conversation(user: int) -> JSON:
    """Shows the conversation with a user."""

    return JSON([message.to_json() for message in get_user_messages(
        CUSTOMER.id, user)])


def write_message() -> JSONMessage:
    """Write a new message."""
    if (reply_to := request.json.get('replyTo')) is not None:
        reply_to = get_user_message(reply_to, user=USER.id)

    recipient = get_user(request.json.get('user'))
    message = Message(parent=reply_to, user=recipient,
                      text=request.json['text'])
    message.save()
    return JSONMessage('Messge added.', id=message.id, status=201)
