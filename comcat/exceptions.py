"""Common exceptions."""


__all__ = ['ComCatException', 'InvalidInitializationToken', 'InvalidSession']


class ComCatException(Exception):
    """Common ComCat exception."""

    pass    # pylint: disable=W0107


class InvalidInitializationToken(ComCatException):
    """Indicates an invalid initialization token."""

    pass    # pylint: disable=W0107


class InvalidSession(ComCatException):
    """Indicates an invalid session."""

    pass    # pylint: disable=W0107
