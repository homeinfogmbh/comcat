"""Common error handlers."""

from comcatlib import UserExpired, UserLocked
from hinews import AccessToken, Article
from hisfs import File
from tenant2tenant import TenantMessage
from wsgilib import JSONMessage, Response, Image


__all__ = ['ERRORS']


ERRORS = {
    Response: lambda response: response,
    JSONMessage: lambda message: message,
    UserExpired: lambda _: JSONMessage('This user is expired.', status=401),
    UserLocked: lambda _: JSONMessage('This user is locked.', status=401),
    AccessToken.DoesNotExist: lambda _: JSONMessage(
        'News not enabled.', status=403),
    Article.DoesNotExist: lambda _: JSONMessage(
        'No such news article.', status=404),
    File.DoesNotExist: lambda _: JSONMessage('No such file.', status=404),
    Image.DoesNotExist: lambda _: JSONMessage(
        'No such news image.', status=404),
    TenantMessage.DoesNotExist: lambda _: JSONMessage(
        'No such tenant message.', status=404)
}
