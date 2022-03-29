"""Contact email management."""

from notificationlib import get_wsgi_funcs

from comcatlib import RegistrationNotificationEmails


__all__ = ['ROUTES']


GET_EMAILS, SET_EMAILS = get_wsgi_funcs(
    'comcat', RegistrationNotificationEmails
)

ROUTES = [('GET', '/email', GET_EMAILS), ('POST', '/email', SET_EMAILS)]
