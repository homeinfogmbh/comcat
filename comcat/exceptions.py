"""Common exceptions."""


__all__ = [
    'ComCatException',
    'InvalidInitializationToken',
    'InvalidSession',
    'NoSuchSession',
    'NoSessionTokenSpecified',
    'InvalidSessionToken']


class ComCatException(Exception):
    """Common ComCat exception."""

    pass    # pylint: disable=W0107


class InvalidInitializationToken(ComCatException):
    """Indicates an invalid initialization token."""

    pass    # pylint: disable=W0107


class InvalidSession(ComCatException):
    """Indicates an invalid session."""

    pass    # pylint: disable=W0107


class NoSuchSession(ComCatException):
    """Indicates that a respective session does not exist."""

    pass    # pylint: disable=W0107


class NoSessionTokenSpecified(ComCatException):
    """Indicates that no session token was specified."""

    pass    # pylint: disable=W0107


class InvalidSessionToken(ComCatException):
    """Indicates that an invalid session token was specified."""

    pass    # pylint: disable=W0107
