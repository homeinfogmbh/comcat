"""Common exceptions and error handlers."""

from comcatlib import UserBaseChart, UserConfiguration, UserMenu
from wsgilib import JSONMessage


__all__ = ['ERRORS']


ERRORS = {
    UserBaseChart.DoesNotExist: lambda _: JSONMessage(
        'No such user base chart.', status=404),
    UserConfiguration.DoesNotExist: lambda _: JSONMessage(
        'No such user configuration.', status=404),
    UserMenu.DoesNotExist: lambda _: JSONMessage(
        'No such user menu.', status=404)
}
