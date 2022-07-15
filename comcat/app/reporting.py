"""Reporting of user-generated content."""

from flask import request

from comcatlib import REQUIRE_OAUTH, TENEMENT, USER
from marketplace import get_offer
from reportlib import report_offer
from reportlib import report_response
from reportlib import report_topic
from reportlib import report_user_event
from tenantcalendar import get_user_event
from tenantforum import get_topic, get_response
from wsgilib import JSONMessage


@REQUIRE_OAUTH('comcat')
def report() -> JSONMessage:
    """Report user-generated content."""

    title = request.json.get('title')
    text = request.json.get('text')
    image = request.json.get('image')

    if 'offer' in request.json:
        report_offer(
            USER.id,
            get_offer(request.json['offer'], customer=TENEMENT.customer),
            title=title,
            text=text,
            image=image
        )
        return JSONMessage('Offer reported.', status=200)

    if 'topic' in request.json:
        report_topic(
            USER.id,
            get_topic(request.json['topic'], customer=TENEMENT.customer),
            title=title,
            text=text,
            image=image
        )
        return JSONMessage('Topic reported.', status=200)

    if 'response' in request.json:
        report_response(
            USER.id,
            get_response(request.json['response'], customer=TENEMENT.customer),
            title=title,
            text=text,
            image=image
        )
        return JSONMessage('Response reported.', status=200)

    if 'event' in request.json:
        report_user_event(
            USER.id,
            get_user_event(request.json['event'], customer=TENEMENT.customer),
            title=title,
            text=text,
            image=image
        )
        return JSONMessage('Event reported.', status=200)

    return JSONMessage('No valid report target selected.', status=400)


ROUTES = [('GET', '/report', report)]
