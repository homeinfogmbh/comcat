"""Local public transport endpoints."""

from comcatlib import REQUIRE_OAUTH, TENEMENT
from lptlib import get_departures as _get_departures
from wsgilib import JSON


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def get_departures() -> JSON:
    """Returns the departures."""

    stops, source = _get_departures(TENEMENT.address)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})


ROUTES = [(['GET'], '/lpt', get_departures)]
