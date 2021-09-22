"""Common error handlers."""

from comcatlib import AlreadyRegistered
from comcatlib import QuotaExceeded
from comcatlib import UserDamageReport
from comcatlib import UserExpired
from comcatlib import UserLocked
from hinews import AccessToken, Article, Image as NewsImage
from hisfs import File
from marketplace import Offer, Image as OfferImage
from tenant2tenant import TenantMessage
from wsgilib import JSONMessage, Response


__all__ = ['ERRORS']


ERRORS = {
    AccessToken.DoesNotExist: lambda _: JSONMessage(
        'News not enabled.', status=403),
    AlreadyRegistered: lambda _: JSONMessage(
        'Already registered.', status=409),
    Article.DoesNotExist: lambda _: JSONMessage(
        'No such news article.', status=404),
    File.DoesNotExist: lambda _: JSONMessage('No such file.', status=404),
    NewsImage.DoesNotExist: lambda _: JSONMessage(
        'No such news image.', status=404),
    JSONMessage: lambda message: message,
    Offer.DoesNotExist: lambda _: JSONMessage('No such offer.', status=404),
    OfferImage.DoesNotExist: lambda _: JSONMessage(
        'No such image.', status=404),
    QuotaExceeded: lambda error: JSONMessage(
        'File quota exceeded.', quota=error.quota, free=error.free,
        size=error.size, status=401),
    Response: lambda response: response,
    TenantMessage.DoesNotExist: lambda _: JSONMessage(
        'No such tenant message.', status=404),
    UserDamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such user damage report.', status=404),
    UserExpired: lambda _: JSONMessage('This user is expired.', status=401),
    UserLocked: lambda _: JSONMessage('This user is locked.', status=401)
}
