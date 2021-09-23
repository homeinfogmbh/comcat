"""Read-only endpoint for data-related files from HISFS."""

from comcatlib import REQUIRE_OAUTH
from hisfs import ERRORS, File
from wsgilib import Binary

from comcat.app.charts import get_base_charts


__all__ = ['ROUTES', 'ERRORS']


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


ROUTES = [(['GET'], '/related-file/<int:ident>', get)]
