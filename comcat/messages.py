"""Web API messages."""

from his.messages import Message


__all__ = ['NoSuchAccount']


class ComCatMessage(Message):
    """Basic ComCat message."""

    DOMAIN = 'comcat'


class NoSuchAccount(ComCatMessage):
    """Indicates that the requested account does not exists."""

    STATUS = 404
