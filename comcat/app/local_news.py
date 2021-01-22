"""Local news endpoint."""

from typing import Iterable, Union

from comcatlib import ADDRESS, CUSTOMER, REQUIRE_OAUTH
from hinews import Article, AccessToken, Image, Tag
from mdb import Address
from wsgilib import Binary, JSON, JSONMessage


__all__ = ['ENDPOINTS']


def _get_address() -> Union[Address, JSONMessage]:
    """Returns the local news address."""

    # Check authorization.
    if AccessToken.get(AccessToken.customer == CUSTOMER.id):
        return ADDRESS

    return JSONMessage('Access token is falsy.', status=500)


def _get_city() -> str:
    """Returns the address's city."""

    return _get_address().city


def _get_local_news_articles() -> Iterable[Article]:
    """Yields local news articles."""

    return Article.select().join(Tag).where(Tag.tag == _get_city())


def _get_local_news_article(article_id: int) -> Article:
    """Yields local news articles."""

    condition = Article.id == article_id
    condition &= Tag.tag == _get_city()
    return Article.select().join(Tag).where(condition).get()


def _get_local_news_image(image_id: int) -> Image:
    """Yields local news articles."""

    condition = Image.id == image_id
    condition &= Tag.tag == _get_city()
    select = Image.select().join(Article).join(Tag)
    return select.where(condition).get()


@REQUIRE_OAUTH('comcat')
def get_local_news_article(article_id: int) -> JSON:
    """Get a single local news article."""

    article = _get_local_news_article(article_id)
    return JSON(article.to_json(preview=True))


@REQUIRE_OAUTH('comcat')
def get_local_news_articles() -> JSON:
    """Lists local news."""

    articles = _get_local_news_articles()
    return JSON([article.to_json(preview=True) for article in articles])


@REQUIRE_OAUTH('comcat')
def get_local_news_image(image_id: int) -> Binary:
    """Returns a local news image."""

    image = _get_local_news_image(image_id)

    try:
        return Binary(image.watermarked)
    except OSError:     # Not an image.
        return Binary(image.data)


ENDPOINTS = (
    (['GET'], '/local-news/<int:article_id>', get_local_news_article,
     'get_news_article'),
    (['GET'], '/local-news', get_local_news_articles, 'list_news_articles'),
    (['GET'], '/local-news/<int:image_id>', get_local_news_image,
     'get_news_image')
)
