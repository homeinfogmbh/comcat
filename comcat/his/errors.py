"""Common exceptions and error handlers."""

from cmslib import AmbiguousConfigurations, NoConfigurationFound
from comcatlib import DuplicateUser
from comcatlib import InvalidAddress
from comcatlib import GroupMemberUser
from comcatlib import MenuBaseChart
from comcatlib import User
from comcatlib import UserBaseChart
from comcatlib import UserConfiguration
from comcatlib import UserDamageReport
from comcatlib import UserMenu
from marketplace import Offer, Image
from mdb import Address, Customer, Tenement
from wsgilib import JSONMessage


__all__ = ['ERRORS']


ERRORS = {
    Address.DoesNotExist: lambda _: JSONMessage(
        'No such address.', status=404),
    AmbiguousConfigurations: lambda _: JSONMessage(
        'Ambiguous configurations.', status=400),
    Customer.DoesNotExist: lambda _: JSONMessage(
        'No such customer.', status=404),
    DuplicateUser: lambda _: JSONMessage('Duplicate user.', 400),
    GroupMemberUser.DoesNotExist: lambda _: JSONMessage(
        'No such group member.', status=404),
    Image.DoesNotExist: lambda _: JSONMessage('No such image.', status=404),
    InvalidAddress: lambda _: JSONMessage(
        'Invalid value for address.', status=400),
    MenuBaseChart.DoesNotExist: lambda _: JSONMessage(
        'No such menu base chart.', status=404),
    NoConfigurationFound: lambda _: JSONMessage(
        'No configuration found.', status=400),
    Offer.DoesNotExist: lambda _: JSONMessage('No such offer.', status=404),
    Tenement.DoesNotExist: lambda _: JSONMessage(
        'The requested tenement does not exist.', status=404),
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
