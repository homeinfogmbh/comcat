"""ComCat end user authentication."""

from functools import wraps

from comcat.contextlocals import SESSION
from comcat.exceptions import NoSuchSession


__all__ = ['authenticated']


def authenticated(function):
    """Prepends authentication checks to the respective function."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the original function."""
        if SESSION.valid:
            return function(*args, **kwargs)

        raise NoSuchSession()

    return wrapper
