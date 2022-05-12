"""Common decorators."""

from functools import wraps
from typing import Callable

from his import CUSTOMER

from comcat.his.functions import get_user


__all__ = ['with_user']


def with_user(function: Callable) -> Callable:
    """Decorator to run the respective function
    with a user as first argument.
    """

    @wraps(function)
    def wrapper(ident: int, *args, **kwargs):
        """Wraps the original function."""
        return function(get_user(ident, CUSTOMER.id), *args, **kwargs)

    return wrapper
