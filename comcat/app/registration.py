"""ComCat user registration."""

from flask import request

from mdb import Customer
from recaptcha import recaptcha
from wsgilib import JSONMessage, require_json

from comcatlib import CONFIG, AlreadyRegistered, UserRegistration

from comcat.app.functions import get_comcat_customer


__all__ = ['ROUTES']


@recaptcha(CONFIG)
@require_json(dict)
def register() -> JSONMessage:
    """Register a new user."""

    try:
        customer = get_comcat_customer(request.json.pop('customer'))
    except Customer.DoesNotExist:
        return JSONMessage('No such customer.', status=404)

    try:
        user_registration = UserRegistration.add(
            request.json['name'], request.json['email'],
            request.json['tenantId'], customer)
    except AlreadyRegistered:
        return JSONMessage('You are already registered.', status=400)

    user_registration.save()
    return JSONMessage('User registered', status=201)


ROUTES = [(['POST'], '/register', register)]
