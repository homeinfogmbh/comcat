"""Local public transport endpoints."""

from flask import request

from comcatlib import REQUIRE_OAUTH, TENEMENT
from lptlib import GeoCoordinates, get_departures
from wsgilib import JSON


__all__ = ['ROUTES']


@REQUIRE_OAUTH('comcat')
def get_home_departures() -> JSON:
    """Returns the departures of the tenenemt address."""

    stops, source = get_departures(TENEMENT.address)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})


@REQUIRE_OAUTH('comcat')
def get_current_departures() -> JSON:
    """Returns the departures of the given geo coordinates."""

    geo = GeoCoordinates(request.json['latitude'], request.json['longitude'])
    stops, source = get_departures(geo)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})


ROUTES = [
    (['GET'], '/lpt/home', get_home_departures),
    (['POST'], '/lpt/current', get_current_departures)
]
