"""Local public transport endpoints."""

from comcatlib import REQUIRE_OAUTH, USER
from lptlib import get_departures as _get_departures
from wsgilib import JSON


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def get_departures():
    """Returns the departures."""

    stops, source = _get_departures(USER.address)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})


ENDPOINTS = ((['GET'], '/lpt', get_departures),)
