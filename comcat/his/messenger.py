"""Comcat messenger."""

from flask import request

from ccmessenger import ERRORS
from ccmessenger import get_attachment
from ccmessenger import get_customer_message
from ccmessenger import get_customer_messages
from ccmessenger import get_user_messages
from ccmessenger import get_user_message
from ccmessenger import Attachment
from ccmessenger import Message
from filedb import File
from his import CUSTOMER, authenticated, authorized
from wsgilib import Binary, JSON, JSONMessage

from comcat.his.functions import get_user


__all__ = ['ERRORS', 'ROUTES']


@authenticated
@authorized('comcat')
def list_messages() -> JSON:
    """Lists messages."""

    return JSON([message.to_json() for message in get_customer_messages(
        CUSTOMER.id)])


@authenticated
@authorized('comcat')
def show_conversation(user: int) -> JSON:
    """Shows the conversation with a user."""

    return JSON([message.to_json() for message in get_user_messages(
       get_user(user))])


@authenticated
@authorized('comcat')
def add_message() -> JSONMessage:
    """Write a new message."""

    recipient = get_user(request.json.get('user'))

    if (reply_to := request.json.get('replyTo')) is not None:
        reply_to = get_user_message(reply_to, user=recipient)

    message = Message(parent=reply_to, user=recipient,
                      text=request.json['text'])
    message.save()
    return JSONMessage('Messge added.', id=message.id, status=201)


@authenticated
@authorized('comcat')
def get_attachment_(ident: int) -> Binary:
    """Returns attachment data."""

    return Binary(get_attachment(ident, customer=CUSTOMER.id).file.bytes)


@authenticated
@authorized('comcat')
def add_attachment(message: int) -> JSONMessage:
    """Adds a new attachment."""

    attachment = Attachment(
        message=get_customer_message(message, customer=CUSTOMER.id),
        file=File.from_bytes(request.get_data(), save=True)
    )
    attachment.save()
    return JSONMessage('Attachment added.', id=attachment.id, status=201)


@authenticated
@authorized('comcat')
def delete_attachment(ident: int) -> JSONMessage:
    """Deletes an attachment."""

    get_attachment(ident, customer=CUSTOMER.id).delete_instance()
    return JSONMessage('Attachment deleted.', status=200)


ROUTES = [
    (['GET'], '/messenger/message', list_messages),
    (['GET'], '/messenger/conversation/<int:user>', show_conversation),
    (['POST'], '/messenger/message', add_message),
    (['GET'], '/messenger/attachment/<int:ident>', get_attachment_),
    (['POST'], '/messenger/attachment/<int:ident>', add_attachment),
    (['DELETE'], '/messenger/attachment/<int:ident>', delete_attachment)
]
