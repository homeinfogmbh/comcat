"""Read-only endpoint for data-related files from HISFS."""

from comcatlib import oauth
from comcatlib.messages import NO_SUCH_FILE
from wsgilib import Binary

from comcat.app.charts import get_user_base_charts


__all__ = ['ENDPOINTS']


def allowed_files():
    """Yields files the current user is allowed to access."""

    files = {}

    for base_chart in get_user_base_charts():
        try:
            for file in base_chart.chart.files:
                files[file.id] = file
        except AttributeError:
            continue

    return files


@oauth('comcat')
def get(ident):
    """Gets a data-related hisfs file."""

    try:
        file = allowed_files()[ident]
    except KeyError:
        return NO_SUCH_FILE

    return Binary(file.bytes)


ENDPOINTS = ((['GET'], '/related-file/<int:ident>', get),)
