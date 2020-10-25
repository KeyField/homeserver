
from mongoengine import Document
from mongoengine.fields import *

from .public_key import PublicKey
from .encryption_key import PublicEncryptionKey

class Homeserver(Document):
    """Represents a peer or detached peer homeserver.
    """
    address = StringField(required=True)
    public_key = LazyReferenceField(PublicKey, passthrough=True, required=True)
    # we can discover the encryption key and name on-demand if we don't yet have it
    name = StringField(required=False)
    encryption_key = LazyReferenceField(PublicEncryptionKey, passthrough=True, required=False)

    def pull_federation_identity(self):
        """Gets the other homeserver's details."""
        pass # TODO

    def get_encryption_key(self):
        """If we don't yet have it, discover it.
        """
        if self.encryption_key is None:
            self.pull_federation_identity()
        return self.encryption_key
