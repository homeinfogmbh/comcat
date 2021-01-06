"""User damage report access."""

from his import authenticated, authorized
from wsgilib import JSON

from comcat.his.functions import get_user_damage_reports


@authenticated
@authorized('comcat')
def list_() -> JSON:
    """Lists damage reports from ComCat accounts."""

    return JSON([
        report.to_json(attachments=True)
        for report in get_user_damage_reports()
    ])


ROUTES = [('GET', '/user_damage_report', list_)]
