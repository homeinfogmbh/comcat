"""ComCat user registration."""

from flask import request

from recaptcha import recaptcha
from wsgilib import JSONMessage, require_json

from comcatlib import CONFIG, UserRegistration


__all__ = ['ROUTES']


@recaptcha(CONFIG)
@require_json(dict)
def register() -> JSONMessage:
    """Register a new user."""

    user_registration = UserRegistration.from_json(request.json)
    user_registration.save()
    return JSONMessage('User registered', status=201)


ROUTES = [(['POST'], '/register', register)]
