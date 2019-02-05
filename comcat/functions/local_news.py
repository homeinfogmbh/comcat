"""Comcat WSGI functions."""

from comcatlib import ACCOUNT
from comcatlib.messages import NO_ADDRESS_CONFIGURED
from comcatlib.messages import NEWS_NOT_ENABLED
from comcatlib.messages import NO_SUCH_ARTICLE
from comcatlib.messages import NO_SUCH_IMAGE
from hinews import Article, AccessToken, Image, Tag


__all__ = ['get_local_news_articles', 'get_local_news_image']


def get_local_news_articles():
    """Yields local news articles."""

    customer = ACCOUNT.customer

    try:
        AccessToken.get(AccessToken.customer == customer)
    except AccessToken.DoesNotExist:
        raise NEWS_NOT_ENABLED

    address = ACCOUNT.address

    if address is None:
        raise NO_ADDRESS_CONFIGURED

    return Article.select().join(Tag).where(Tag.tag == address.city)


def get_local_news_image(article_id, image_id):
    """Yields local news articles."""

    customer = ACCOUNT.customer

    try:
        AccessToken.get(AccessToken.customer == customer)
    except AccessToken.DoesNotExist:
        raise NEWS_NOT_ENABLED

    address = ACCOUNT.address

    if address is None:
        raise NO_ADDRESS_CONFIGURED

    try:
        article = Article.select().join(Tag).where(
            (Tag.tag == address.city) & (Article.id == article_id))
    except Article.DoesNotExist:
        raise NO_SUCH_ARTICLE

    try:
        return Image.select().where(
            (Image.article == article) & (Image.id == image_id))
    except Image.DoesNotExist:
        raise NO_SUCH_IMAGE
