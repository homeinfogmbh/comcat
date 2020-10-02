"""Meta backend."""

from comcatlib import REQUIRE_OAUTH, USER, InitializationNonce


__all__ = ['ENDPOINTS']


@REQUIRE_OAUTH('comcat')
def generate_initialization_nonce():
    """Generates a new initialization nonce."""

    try:
        nonce = InitializationNonce.get(InitializationNonce.user == USER.id)
    except InitializationNonce.DoesNotExist:
        nonce = InitializationNonce.add(user=USER.id)

    return nonce.uuid.hex


ENDPOINTS = [(['GET'], '/initnonce', generate_initialization_nonce)]
