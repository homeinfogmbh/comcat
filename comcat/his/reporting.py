"""User-generated content reports management."""

from comcatlib import User
from his import CUSTOMER, authenticated, authorized
from mdb import Tenement
from reportlib import OfferReport, TopicReport, ResponseReport, UserEventReport
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('comcat')
def list_offer_reports() -> JSON:
    """List offer reports."""

    return JSON([
        report.to_json() for report
        in OfferReport.select().join(User).join(Tenement).where(
            Tenement.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def list_topic_reports() -> JSON:
    """List topic reports."""

    return JSON([
        report.to_json() for report
        in TopicReport.select().join(User).join(Tenement).where(
            Tenement.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def list_response_reports() -> JSON:
    """List offer reports."""

    return JSON([
        report.to_json() for report
        in ResponseReport.select().join(User).join(Tenement).where(
            Tenement.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def list_user_event_reports() -> JSON:
    """List user event reports."""

    return JSON([
        report.to_json() for report
        in UserEventReport.select().join(User).join(Tenement).where(
            Tenement.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('comcat')
def delete_offer_report(ident: int) -> JSONMessage:
    """Remove the respective offer report."""

    OfferReport.select().join(User).join(Tenement).where(
        (Tenement.customer == CUSTOMER.id)
        & (OfferReport.id == ident)
    ).get().delete_instance()
    return JSONMessage('Offer report deleted.', status=200)


@authenticated
@authorized('comcat')
def delete_topic_report(ident: int) -> JSONMessage:
    """Remove the respective topic report."""

    TopicReport.select().join(User).join(Tenement).where(
        (Tenement.customer == CUSTOMER.id)
        & (TopicReport.id == ident)
    ).get().delete_instance()
    return JSONMessage('Topic report deleted.', status=200)


@authenticated
@authorized('comcat')
def delete_response_report(ident: int) -> JSONMessage:
    """Remove the respective response report."""

    ResponseReport.select().join(User).join(Tenement).where(
        (Tenement.customer == CUSTOMER.id)
        & (ResponseReport.id == ident)
    ).get().delete_instance()
    return JSONMessage('Response report deleted.', status=200)


@authenticated
@authorized('comcat')
def delete_user_event_report(ident: int) -> JSONMessage:
    """Remove the respective user event report."""

    UserEventReport.select().join(User).join(Tenement).where(
        (Tenement.customer == CUSTOMER.id)
        & (UserEventReport.id == ident)
    ).get().delete_instance()
    return JSONMessage('Event report deleted.', status=200)


ROUTES = [
    ('GET', '/reporting/offer', list_offer_reports),
    ('GET', '/reporting/topic', list_topic_reports),
    ('GET', '/reporting/response', list_response_reports),
    ('GET', '/reporting/event', list_user_event_reports),
    ('DELETE', '/reporting/offer/<int:ident>', delete_offer_report),
    ('DELETE', '/reporting/topic/<int:ident>', delete_topic_report),
    ('DELETE', '/reporting/response/<int:ident>', delete_response_report),
    ('DELETE', '/reporting/event/<int:ident>', delete_user_event_report),
]
