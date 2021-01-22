"""Common error handlers."""

from comcatlib import UserExpired, UserLocked
from hinews import AccessToken
from wsgilib import JSONMessage, Response


__all__ = ['ERRORS']


ERRORS = {
    Response: lambda response: response,
    JSONMessage: lambda message: message,
    UserExpired: lambda _: JSONMessage('This user is expired.', status=401),
    UserLocked: lambda _: JSONMessage('This user is locked.', status=401),
    AccessToken.DoesNotExist: lambda _: JSONMessage
}
