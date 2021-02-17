"""Common functions."""

from comcatlib import Token, User


__all__ = ['logout']


def logout(user: User):
    """Logs out a user."""

    return Token.delete().where(Token.user == user).execute()
