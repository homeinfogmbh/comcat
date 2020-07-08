"""User files endpoint."""

from functools import wraps

from flask import request

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH
from comcatlib.messages import NO_SUCH_FILE
from comcatlib.orm.files import File, Quota
from hisfs.exceptions import QuotaExceeded
from hisfs.messages import FILE_CREATED, FILE_DELETED, QUOTA_EXCEEDED
from wsgilib import Binary, JSON


__all__ = ['ENDPOINTS', 'get_file']


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
    def wrapper(ident, *args, **kwargs):
        """Wraps the decorated function."""
        return function(get_file(ident), *args, **kwargs)

    return wrapper


@REQUIRE_OAUTH('comcat')
def post():
    """Adds a new file."""

    bytes_ = request.get_data()
    quota = Quota.for_customer(current_token.user.customer_id)

    try:
        quota.alloc(len(bytes_))
    except QuotaExceeded:
        return QUOTA_EXCEEDED

    file = File.add(current_token.user, bytes_)
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
    """Deletes a user file."""

    file.delete_instance()
    return FILE_DELETED


ENDPOINTS = (
    (['POST'], '/user-file', post),
    (['GET'], '/user-file/<int:ident>', get),
    (['DELETE'], '/user-file/<int:ident>', delete)
)
