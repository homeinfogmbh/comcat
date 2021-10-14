"""ComCat user registration."""

from flask import request

from mdb import Customer
from recaptcha import recaptcha
from wsgilib import JSONMessage, require_json

from comcatlib import CONFIG, UserRegistration

from comcat.app.functions import get_comcat_customer


__all__ = ['ROUTES']


REGISTRATION_SUCCEEDED = JSONMessage('User registered', status=201)


@recaptcha(CONFIG)
@require_json(dict)
def register() -> JSONMessage:
    """Register a new user."""

    try:
        customer = get_comcat_customer(request.json.pop('customer'))
    except Customer.DoesNotExist:
        return REGISTRATION_SUCCEEDED

    user_registration = UserRegistration.from_json(request.json, customer)
    user_registration.save()
    return REGISTRATION_SUCCEEDED


ROUTES = [(['POST'], '/register', register)]
