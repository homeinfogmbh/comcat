"""User files endpoint."""

from functools import wraps

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, add_file, UserFile
from comcatlib.messages import NO_SUCH_FILE
from hisfs.messages import FILE_CREATED, FILE_DELETED
from wsgilib import Binary, JSON


__all__ = ['ENDPOINTS', 'get_file']


def get_file(file_id):
    """Returns the file with the given ID."""

    condition = UserFile.id == file_id
    condition &= UserFile.user == USER.id

    try:
        return UserFile.get(condition)
    except UserFile.DoesNotExist:
        raise NO_SUCH_FILE from None


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
    user_file = add_file(bytes_)
    return FILE_CREATED.update(id=user_file.id)


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
