"""Tenant forum endpoints."""

from flask import request

from comcatlib import REQUIRE_OAUTH, USER
from tenantforum import ERRORS
from tenantforum import get_visible_topics
from tenantforum import get_visible_topic
from tenantforum import get_own_topics
from tenantforum import get_own_topic
from tenantforum import get_visible_responses
from tenantforum import get_own_responses
from tenantforum import get_own_response
from tenantforum import Topic
from tenantforum import Response
from wsgilib import JSON, JSONMessage


__all__ = ["ROUTES", "ERRORS"]


@REQUIRE_OAUTH("comcat")
def list_topics() -> JSON:
    """Lists visible topics."""

    return JSON([topic.to_json() for topic in get_visible_topics(USER)])


@REQUIRE_OAUTH("comcat")
def list_own_topics() -> JSON:
    """Lists own topics."""

    return JSON([topic.to_json() for topic in get_own_topics(USER)])


@REQUIRE_OAUTH("comcat")
def list_responses(topic: int) -> JSON:
    """Lists responses of a topic."""

    return JSON([response.to_json() for response in get_visible_responses(topic, USER)])


@REQUIRE_OAUTH("comcat")
def list_own_responses() -> JSON:
    """Lists own responses."""

    return JSON([response.to_json() for response in get_own_responses(USER)])


@REQUIRE_OAUTH("comcat")
def add_topic() -> JSONMessage:
    """Adds a new topic."""

    topic = Topic.from_json(request.json, user=USER.id)
    topic.save()
    return JSONMessage("Topic created.", id=topic.id, status=201)


@REQUIRE_OAUTH("comcat")
def add_response() -> JSONMessage:
    """Adds a new topic."""

    topic = get_visible_topic(request.json.pop("topic"), USER)
    response = Response.from_json(request.json, user=USER.id, topic=topic)
    response.save()
    return JSONMessage("Response created.", id=topic.id, status=201)


@REQUIRE_OAUTH("comcat")
def edit_topic(ident: int) -> JSONMessage:
    """Edits a topic."""

    topic = get_own_topic(ident, USER)
    topic.patch_json(request.json)
    topic.save()
    return JSONMessage("Topic edited.", status=200)


@REQUIRE_OAUTH("comcat")
def edit_response(ident: int) -> JSONMessage:
    """Edits a response."""

    response = get_own_response(ident, USER)
    response.patch_json(request.json)
    response.save()
    return JSONMessage("Response edited.", status=200)


@REQUIRE_OAUTH("comcat")
def delete_topic(ident: int) -> JSONMessage:
    """Deletes a topic."""

    get_own_topic(ident, user=USER).delete_instance()
    return JSONMessage("Topic deleted.", status=200)


@REQUIRE_OAUTH("comcat")
def delete_response(ident: int) -> JSONMessage:
    """Deletes a response."""

    response = get_own_response(ident, user=USER)
    response.text = None
    response.save()
    return JSONMessage("Response deleted.", status=200)


ROUTES = [
    (["GET"], "/tenantforum/topic", list_topics),
    (["GET"], "/tenantforum/topic/own", list_own_topics),
    (["GET"], "/tenantforum/response/<int:topic>", list_responses),
    (["GET"], "/tenantforum/response/own", list_own_responses),
    (["POST"], "/tenantforum/topic", add_topic),
    (["POST"], "/tenantforum/response", add_response),
    (["PATCH"], "/tenantforum/topic/<int:ident>", edit_topic),
    (["PATCH"], "/tenantforum/response/<int:ident>", edit_response),
    (["DELETE"], "/tenantforum/topic/<int:ident>", delete_topic),
    (["DELETE"], "/tenantforum/response/<int:ident>", delete_response),
]
