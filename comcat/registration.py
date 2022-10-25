"""ComCat user registration."""

from flask import request

from mdb import Customer
from mtcaptcha import mtcaptcha
from wsgilib import JSONMessage, require_json

from comcatlib import AlreadyRegistered
from comcatlib import UserRegistration
from comcatlib import get_config
from comcatlib import notify_customer
from comcatlib import notify_user

from comcat.functions import get_comcat_customer


__all__ = ['ROUTES']


@mtcaptcha(
    lambda: request.json.pop('response'),
    lambda: get_config().get('mtcaptcha', 'private_key')
)
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
            request.json['tenantId'], customer
        )
    except AlreadyRegistered as error:
        return JSONMessage(
            'You are already registered.', email=error.email, status=400
        )

    user_registration.save()
    notify_user(user_registration.email)
    notify_customer(user_registration)
    return JSONMessage('User registered.', status=201)


ROUTES = [(['POST'], '/register', register)]
