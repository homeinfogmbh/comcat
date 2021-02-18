"""User files endpoint."""

from flask import request

from comcatlib import REQUIRE_OAUTH, add_file, UserFile
from wsgilib import Binary, JSON, JSONMessage

from comcat.app.functions import with_user_file


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def post() -> JSONMessage:
    """Adds a new file."""

    bytes_ = request.get_data()
    user_file = add_file(bytes_)
    return JSONMessage(
        'User file added.', id=user_file.id, file=user_file.file_id,
        status=201)


@REQUIRE_OAUTH('comcat')
@with_user_file
def get(user_file: UserFile) -> JSONMessage:
    """Returns a user file."""

    if request.args.get('metadata'):
        return JSON(user_file.to_json())

    if request.args.get('download'):
        return Binary(user_file.bytes, filename=user_file.name)

    return Binary(user_file.bytes)


@REQUIRE_OAUTH('comcat')
@with_user_file
def delete(user_file: UserFile) -> JSONMessage:
    """Deletes a user file."""

    user_file.delete_instance()
    return JSONMessage('User file deleted.', status=200)


ENDPOINTS = [
    (['POST'], '/user-file', post, 'add_user_file'),
    (['GET'], '/user-file/<int:ident>', get, 'get_user_file'),
    (['DELETE'], '/user-file/<int:ident>', delete, 'delete_user_file')
]
