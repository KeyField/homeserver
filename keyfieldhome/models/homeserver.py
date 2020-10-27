
from mongoengine import Document
from mongoengine.fields import *

from .public_key import PublicKeyPair

class Homeserver(Document):
    """Represents a peer or detached peer homeserver.
    """
    address = StringField(required=True, unique=True)
    server_key = EmbeddedDocumentField(PublicKeyPair, required=True)
    # we can discover the encryption key and name on-demand if we don't yet have it
    name = StringField()
    server_username = StringField()

    def pull_federation_identity(self):
        """Updates the other homeserver's details."""
        pass # TODO

    @property
    def publickey(self):
        """If we don't yet have it, discover it.

        If a server encryption key ever changes then manual intervention is required.
        (Something very bad might have happened)
        """
        if self.server_key.publickey_bytes is None:
            self.pull_federation_identity()
        return self.server_key.publickey
