"""ComCat login."""


def login():
    """Logs in an end user."""

    user_name = request.json.get('user_name')

    if not user_name:
        return NoUserNameSpecified()

    passwd = request.json.get('passwd')

    if not passwd:
        return NoPasswordSpecified()

    try:
        account = Account.get(Account.name = user_name)
    except Account.DoesNotExist:
        return InvalidCredentials()     # Mitigate account spoofing.

    if account.login(passwd):
        session = Session.open(account, duration=_get_duration())
        return JSON(session.to_json())

    return InvalidCredentials()
