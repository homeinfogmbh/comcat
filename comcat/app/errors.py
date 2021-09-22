"""Common error handlers."""

from comcatlib import AlreadyRegistered
from comcatlib import QuotaExceeded
from comcatlib import UserDamageReport
from comcatlib import UserExpired
from comcatlib import UserLocked
from wsgilib import JSONMessage, Response


__all__ = ['ERRORS']


ERRORS = {
    AlreadyRegistered: lambda _: JSONMessage(
        'Already registered.', status=409),
    JSONMessage: lambda message: message,
    QuotaExceeded: lambda error: JSONMessage(
        'File quota exceeded.', quota=error.quota, free=error.free,
        size=error.size, status=401),
    Response: lambda response: response,
    UserDamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such user damage report.', status=404),
    UserExpired: lambda _: JSONMessage('This user is expired.', status=401),
    UserLocked: lambda _: JSONMessage('This user is locked.', status=401)
}
