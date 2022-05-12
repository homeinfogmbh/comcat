"""User damage report access."""

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_user_damage_reports


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists damage reports from ComCat accounts."""

    return JSON([
        report.to_json() for report in get_user_damage_reports(CUSTOMER.id)
    ])


ROUTES = [('GET', '/user_damage_report', list_)]
