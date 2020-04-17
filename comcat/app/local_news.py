"""Local news endpoint."""

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from comcatlib.messages import NEWS_NOT_ENABLED
from comcatlib.messages import NO_SUCH_ARTICLE
from comcatlib.messages import NO_SUCH_ARTICLE_IMAGE
from hinews import Article, AccessToken, Image, Tag
from wsgilib import Binary, JSON


__all__ = ['get_local_news_articles', 'get_local_news_image']


def _get_address():
    """Returns the local news address."""

    try:
        AccessToken.get(AccessToken.customer == current_token.user.customer)
    except AccessToken.DoesNotExist:
        raise NEWS_NOT_ENABLED

    try:
        address = current_token.user.tenement.address
    except AttributeError:
        raise NO_ADDRESS_CONFIGURED

    if address is None:
        raise NO_ADDRESS_CONFIGURED

    return address


def _get_city():
    """Returns the address's city."""

    return _get_address().city


def _get_local_news_articles():
    """Yields local news articles."""

    return Article.select().join(Tag).where(Tag.tag == _get_city())


def _get_local_news_article(article_id):
    """Yields local news articles."""

    condition = Article.id == article_id
    condition &= Tag.tag == _get_city()

    try:
        article = Article.select().join(Tag).where(condition).get()
    except Article.DoesNotExist:
        raise NO_SUCH_ARTICLE


def _get_local_news_image(article_id, image_id):
    """Yields local news articles."""

    condition = Image.id == image_id
    condition &= Image.article == _get_local_news_article(article_id)

    try:
        return Image.select().where(condition).get()
    except Image.DoesNotExist:
        raise NO_SUCH_ARTICLE_IMAGE


@REQUIRE_OAUTH('comcat')
def get_local_news_articles():
    """Lists local news."""

    return JSON([
        article.to_json(preview=True) for article
        in _get_local_news_articles()])


@REQUIRE_OAUTH('comcat')
def get_local_news_image(article_id, image_id):
    """Returns a local news image."""

    image = _get_local_news_image(article_id, image_id)

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.data)
