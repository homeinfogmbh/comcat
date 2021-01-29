"""Common exceptions and error handlers."""

from cmslib import AmbiguousConfigurationsError, NoConfigurationFound
from comcatlib import DuplicateUser
from comcatlib import InvalidAddress
from comcatlib import GroupMemberUser
from comcatlib import User
from comcatlib import UserBaseChart
from comcatlib import UserConfiguration
from comcatlib import UserDamageReport
from comcatlib import UserMenu
from mdb import Address, Customer, Tenement
from wsgilib import JSONMessage


__all__ = ['ERRORS']


ERRORS = {
    Address.DoesNotExist: lambda _: JSONMessage(
        'No such address.', status=404),
    AmbiguousConfigurationsError: lambda _: JSONMessage(
        'Ambiguous configurations.', status=400),
    Customer.DoesNotExist: lambda _: JSONMessage(
        'No such customer.', status=404),
    DuplicateUser: lambda _: JSONMessage('Duplicate user.', 400),
    GroupMemberUser.DoesNotExist: lambda _: JSONMessage(
        'No such group member.', status=404),
    InvalidAddress: lambda _: JSONMessage(
        'Invalid value for address.', status=400),
    NoConfigurationFound: lambda _: JSONMessage(
        'No configuration found.', status=400),
    Tenement.DoesNotExist: lambda _: JSONMessage(
        'The requested tenement does not eixst.', status=404),
    User.DoesNotExist: lambda _: JSONMessage(
        'No such user.', status=404),
    UserBaseChart.DoesNotExist: lambda _: JSONMessage(
        'No such user base chart.', status=404),
    UserConfiguration.DoesNotExist: lambda _: JSONMessage(
        'No such user configuration.', status=404),
    UserDamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such user damage report.', status=404),
    UserMenu.DoesNotExist: lambda _: JSONMessage(
        'No such user menu.', status=404)
}
