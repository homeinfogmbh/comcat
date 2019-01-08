"""Interface for the end-user applications."""


from comcat.auth import authenticated


def login():
    """ Performs a login."""
    # TODO: Implement.
    pass


@authenticated
def get_news():

    pass
