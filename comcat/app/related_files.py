"""Read-only endpoint for data-related files from HISFS."""

from comcatlib import REQUIRE_OAUTH
from comcatlib.messages import NO_SUCH_FILE
from wsgilib import Binary

from comcat.app.charts import get_user_base_charts


__all__ = ['ENDPOINTS']


class NoSuchFile(Exception):
    """Indicates that the respective file could not be found."""


def get_file(ident):
    """Yields files the current user is allowed to access."""

    for base_chart in get_user_base_charts():
        try:
            files = base_chart.chart.files
        except AttributeError:
            continue

        for file in files:
            if file.id == ident:
                return file

    raise NoSuchFile()


@REQUIRE_OAUTH('comcat')
def get(ident):
    """Gets a data-related hisfs file."""

    try:
        file = get_file(ident)
    except NoSuchFile:
        return NO_SUCH_FILE

    return Binary(file.bytes)


ENDPOINTS = [(['GET'], '/related-file/<int:ident>', get, 'get_related_file')]
