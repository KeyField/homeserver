
from mongoengine import Document
from mongoengine.fields import *
from nacl.encoding import URLSafeBase64Encoder

from ..utils import get_timestamp_seconds
from .public_key import PublicKeyPair

class Homeserver(Document):
    """Represents a peer or detached peer homeserver.
    """
    address = StringField(required=True, unique=True)
    server_key = EmbeddedDocumentField(PublicKeyPair, required=True)
    # we can discover the encryption key and name on-demand if we don't yet have it
    name = StringField()
    server_username = StringField()
    # counter for failure to federate with, bad signature, request denied, etc...
    failcount = IntField()

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

    @property
    def verifykey(self):
        return self.server_key.verifykey

    @property
    def identityblock_homeserver(self):
        """The homeserver section of the identity block."""
        return {
            "address": self.address,
            "verify": self.verifykey.encode(URLSafeBase64Encoder).decode(),
            "public": self.publickey.encode(URLSafeBase64Encoder).decode(),
            # "timestamp": get_timestamp_seconds(),
        }
