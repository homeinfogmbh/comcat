"""Local public transport endpoints."""

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH
from lptlib import get_departures as _get_departures
from wsgilib import JSON


__all__ = ['get_departures']


@REQUIRE_OAUTH('comcat')
def get_departures():
    """Returns the departures."""

    address = current_token.user.address
    stops, source = _get_departures(address)
    stops = [stop.to_json() for stop in stops]
    return JSON({'source': source, 'stops': stops})
