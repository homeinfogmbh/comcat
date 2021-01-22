"""User files endpoint."""

from functools import wraps

from flask import request

from comcatlib import REQUIRE_OAUTH, USER, add_file, UserFile
from comcatlib.messages import NO_SUCH_FILE
from hisfs.messages import FILE_CREATED, FILE_DELETED
from wsgilib import Binary, JSON


__all__ = ['ENDPOINTS', 'get_user_file']


def get_user_file(ident):
    """Returns the user file with the given ID."""

    condition = UserFile.user == USER.id

    if request.args.get('direct', False):
        condition &= UserFile.file == ident
    else:
        condition &= UserFile.id == ident

    try:
        return UserFile.get(condition)
    except UserFile.DoesNotExist:
        raise NO_SUCH_FILE from None


def with_user_file(function):
    """Returns the respective user file."""

    @wraps(function)
    def wrapper(ident, *args, **kwargs):
        """Wraps the decorated function."""
        return function(get_user_file(ident), *args, **kwargs)

    return wrapper


@REQUIRE_OAUTH('comcat')
def post():
    """Adds a new file."""

    bytes_ = request.get_data()
    user_file = add_file(bytes_)
    return FILE_CREATED.update(id=user_file.id, file=user_file.file_id)


@REQUIRE_OAUTH('comcat')
@with_user_file
def get(user_file):
    """Returns a user file."""

    if request.args.get('metadata'):
        return JSON(user_file.to_json())

    if request.args.get('download'):
        return Binary(user_file.bytes, filename=user_file.name)

    return Binary(user_file.bytes)


@REQUIRE_OAUTH('comcat')
@with_user_file
def delete(user_file):
    """Deletes a user file."""

    user_file.delete_instance()
    return FILE_DELETED


ENDPOINTS = (
    (['POST'], '/user-file', post, 'add_user_file'),
    (['GET'], '/user-file/<int:ident>', get, 'get_user_file'),
    (['DELETE'], '/user-file/<int:ident>', delete, 'delete_user_file')
)
