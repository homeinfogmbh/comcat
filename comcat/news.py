"""News interface."""

from comcatlib import CUSTOMER, REQUIRE_OAUTH
from filedb import File
from newslib import articles
from wsgilib import Binary, JSON


__all__ = ["ROUTES"]


@REQUIRE_OAUTH("comcat")
def list_articles() -> JSON:
    """List news articles that the customer may access."""

    return JSON([article.to_json() for article in articles(CUSTOMER.id)])


@REQUIRE_OAUTH("comcat")
def get_image(ident: int) -> Binary:
    """Returns the respective file."""

    return Binary(get_file(ident).bytes)


def get_file(ident: int) -> File:
    """Yields files the current user is allowed to access."""
    if ident in {
        article.image.id
        for article in articles(CUSTOMER.id)
        if article.image is not None
    }:
        return File.get(File.id == ident)

    raise File.DoesNotExist()


ROUTES = [
    (["GET"], "/news", list_articles),
    (["GET"], "/news-image/<int:ident>", get_image),
]
