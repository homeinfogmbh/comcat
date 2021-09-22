"""Damage report related errors."""

from damage_report import Attachment, DamageReport
from wsgilib import JSONMessage


__all__ = ['ERRORS']


ERRORS = {
    Attachment.DoesNotExist: lambda _: JSONMessage(
        'No such attachment.', status=404),
    DamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such damage report.', status=404)
}
