"""Common error handlers."""

from comcatlib import AlreadyRegistered
from comcatlib import QuotaExceeded
from comcatlib import UserDamageReport
from comcatlib import UserExpired
from comcatlib import UserLocked
from filedb import File
from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from wsgilib import JSONMessage, Response


__all__ = ["ERRORS"]


ERRORS = {
    AlreadyRegistered: lambda error: JSONMessage(
        "Already registered.", email=error.email, status=409
    ),
    FieldNotNullable: lambda error: JSONMessage(
        "Field not nullable.", model=error.model.__name__, key=error.key, status=400
    ),
    FieldValueError: lambda error: JSONMessage(
        "Field value error.",
        model=error.model.__name__,
        key=error.key,
        value=str(error.value),
        status=400,
    ),
    File.DoesNotExist: lambda error: JSONMessage("No such file.", status=404),
    InvalidKeys: lambda error: JSONMessage(
        "Invalid keys.", keys=error.invalid_keys, status=400
    ),
    MissingKeyError: lambda error: JSONMessage(
        "Invalid keys.", model=error.model.__name__, key=error.key, status=400
    ),
    NonUniqueValue: lambda error: JSONMessage(
        "Non-unique value", key=error.key, value=error.value, status=400
    ),
    JSONMessage: lambda message: message,
    QuotaExceeded: lambda error: JSONMessage(
        "File quota exceeded.",
        quota=error.quota,
        free=error.free,
        size=error.size,
        status=401,
    ),
    Response: lambda response: response,
    UserDamageReport.DoesNotExist: lambda _: JSONMessage(
        "No such user damage report.", status=404
    ),
    UserExpired: lambda _: JSONMessage("This user is expired.", status=401),
    UserLocked: lambda _: JSONMessage("This user is locked.", status=401),
}
