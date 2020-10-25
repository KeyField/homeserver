
from mongoengine import Document
from mongoengine.fields import *
import bson
from nacl.public import Box


class PublicEncryptionKey(Document):
    """Represents the public part of an encryption keypair.

    The private part can be held by a User, Homeserver, or Device.
    """
    key_bytes = BinaryField(required=True)
    created = DateTimeField()
    expires = DateTimeField()

    def encrypt_to(self, content: bytes):
        """Encrypts data for this key with this homeserver's private key."""
        pass # TODO
