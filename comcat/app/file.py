"""Attachment file endpoint."""

from functools import wraps

from flask import request

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH
from comcatlib.messages import NO_SUCH_FILE
from hisfs.exceptions import QuotaExceeded
from hisfs.messages import FILE_CREATED, FILE_DELETED, QUOTA_EXCEEDED
from hisfs.orm import File, Quota
from wsgilib import Binary, JSON


__all__ = ['ENDPOINTS']


def get_file(file_id):
    """Returns the file with the given ID."""

    condition = File.id == file_id

    if not current_token.user.root:
        condition &= File.user == current_token.user

    try:
        return File.get(condition)
    except File.DoesNotExist:
        raise NO_SUCH_FILE


def with_file(function):
    """Returns the respective file."""

    @wraps(function)
    def wrapper(file_id, *args, **kwargs):
        """Wraps the decorated function."""
        return function(get_file(file_id), *args, **kwargs)

    return wrapper


@REQUIRE_OAUTH('comcat')
def post(name):
    """Adds a new file."""

    bytes_ = request.get_data()

    try:
        Quota.for_customer(current_token.user.customer_id).alloc(len(bytes_))
    except QuotaExceeded:
        return QUOTA_EXCEEDED

    file = File.add(name, current_token.user, bytes_)
    file.save()
    return FILE_CREATED.update(id=file.id)


@REQUIRE_OAUTH('comcat')
@with_file
def get(file):
    """Returns an image file from the
    presentation for the respective account.
    """

    if request.args.get('metadata'):
        return JSON(file.metadata.to_json())

    if request.args.get('download'):
        return Binary(file.bytes, filename=file.name)

    return Binary(file.bytes)


@REQUIRE_OAUTH('comcat')
@with_file
def delete(file):
    """Returns an image file from the
    presentation for the respective account.
    """

    file.delete_instance()
    return FILE_DELETED


ENDPOINTS = (
    (['POST'], '/file', post),
    (['GET'], '/file/<int:file_id>', post),
    (['DELETE'], '/file/<int:file_id>', delete)
)
