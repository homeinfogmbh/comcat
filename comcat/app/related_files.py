"""Read-only endpoint for data-related files from HISFS."""

from comcatlib import REQUIRE_OAUTH
from hisfs import File
from wsgilib import Binary, JSONMessage

from comcat.app.charts import get_base_charts


__all__ = ['ENDPOINTS', 'ERRORS']


ERRORS = {File.DoesNotExist: lambda _: JSONMessage('No such file.', status=404)}


def get_file(ident: int):
    """Yields files the current user is allowed to access."""

    for base_chart in get_base_charts():
        try:
            files = base_chart.chart.files
        except AttributeError:
            continue

        if ident in files:
            return File.select(cascade=True).where(File.id == ident).get()

    raise File.DoesNotExist()


@REQUIRE_OAUTH('comcat')
def get(ident):
    """Gets a data-related hisfs file."""

    return Binary(get_file(ident).bytes)


ENDPOINTS = [(['GET'], '/related-file/<int:ident>', get, 'get_related_file')]
