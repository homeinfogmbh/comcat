"""Attachment file endpoint."""

from authlib.integrations.flask_oauth2 import current_token

from comcatlib import REQUIRE_OAUTH
from comcatlib import Presentation
from comcatlib.messages import NO_SUCH_FILE
from hisfs import File
from wsgilib import Binary


__all__ = ['get_file']


@REQUIRE_OAUTH('comcat')
def get_file(file):
    """Returns an image file from the
    presentation for the respective account.
    """

    presentation = Presentation(current_token.user)

    if file in presentation.files:
        try:
            file = File[file]
        except File.DoesNotExist:
            raise NO_SUCH_FILE

        return Binary(file.bytes)

    raise NO_SUCH_FILE  # Mitigate file sniffing.
