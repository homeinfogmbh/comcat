"""Tenant forum administration."""

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage

from tenantforum import ERRORS
from tenantforum import get_topics
from tenantforum import get_topic
from tenantforum import get_responses
from tenantforum import get_response


__all__ = ['ROUTES', 'ERRORS']


@authenticated
@authorized('comcat')
def list_topics() -> JSON:
    """Lists topics of the current customer."""

    return JSON([topic.to_json() for topic in get_topics(CUSTOMER)])


@authenticated
@authorized('comcat')
def list_responses(topic: int) -> JSON:
    """Lists responses of the given topic and current customer."""

    return JSON([
        response.to_json() for response in get_responses(topic, CUSTOMER)
    ])


@authenticated
@authorized('comcat')
def delete_topic(ident: int) -> JSONMessage:
    """Removes the given topic of the current customer."""

    get_topic(ident, CUSTOMER).delete_instance()
    return JSONMessage('Topic deleted.', status=200)


@authenticated
@authorized('comcat')
def delete_response(ident: int) -> JSONMessage:
    """Removes the given response of the current customer."""

    get_response(ident, CUSTOMER).delete_instance()
    return JSONMessage('Response deleted.', status=200)


ROUTES = [
    ('GET', '/tenantforum/topic', list_topics),
    ('GET', '/tenantforum/response/<int:topic>', list_responses),
    ('DELETE', '/tenantforum/topic/<int:ident>', delete_topic),
    ('DELETE', '/tenantforum/response/<int:ident>', delete_response)
]
