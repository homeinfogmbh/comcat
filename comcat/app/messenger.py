"""Comcat messenger."""

from flask import request

from ccmessenger import get_attachment, get_user_message, get_user_messages
from ccmessenger import Attachment
from ccmessenger import Message
from comcatlib import REQUIRE_OAUTH, USER
from filedb import File
from wsgilib import Binary, JSON, JSONMessage


__all__ = ['ERRORS', 'ROUTES']


ERRORS = {
    Message.DoesNotExist: lambda _: JSONMessage(
        'No such message.', status=404),
    Attachment.DoesNotExist: lambda _: JSONMessage(
        'No such attachment.', status=404)
}


@REQUIRE_OAUTH('comcat')
def list_messages() -> JSON:
    """Lists messages of the current user."""

    return JSON([message.to_json() for message in get_user_messages(USER.id)])


@REQUIRE_OAUTH('comcat')
def add_message() -> JSONMessage:
    """Adds a new message."""

    if (reply_to := request.json.get('replyTo')) is not None:
        reply_to = get_user_message(reply_to, user=USER.id)

    message = Message(parent=reply_to, user=USER.id, text=request.json['text'])
    message.save()
    return JSONMessage('Messge added.', id=message.id, status=201)


@REQUIRE_OAUTH('comcat')
def get_attachment_(ident: int) -> Binary:
    """Returns attachment data."""

    return Binary(get_attachment(ident, user=USER.id).file.bytes)


@REQUIRE_OAUTH('comcat')
def add_attachment(message: int) -> JSONMessage:
    """Adds a new attachment."""

    attachment = Attachment(
        message=get_user_message(message, USER.id, own=True),
        file=File.from_bytes(request.get_data(), save=True)
    )
    attachment.save()
    return JSONMessage('Attachment added.', id=attachment.id, status=201)


@REQUIRE_OAUTH('comcat')
def delete_attachment(ident: int) -> JSONMessage:
    """Deletes an attachment."""

    get_attachment(ident, user=USER.id, own=True).delete_instance()
    return JSONMessage('Attachment deleted.', status=200)


ROUTES = [
    (['GET'], '/messenger/message', list_messages),
    (['POST'], '/messenger/message', add_message),
    (['GET'], '/messenger/attachment/<int:ident>', get_attachment_),
    (['POST'], '/messenger/attachment/<int:ident>', add_attachment),
    (['DELETE'], '/messenger/attachment/<int:ident>', delete_attachment)
]
