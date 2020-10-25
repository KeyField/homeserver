
from mongoengine import Document
from mongoengine.fields import *
import bson
from nacl.signing import VerifyKey


class PublicKey(Document):
    """Represents the public part of a signing keypair.

    The private part can be held by a User, Homeserver, or Device.
    """
    key_bytes = BinaryField(required=True)
    created = DateTimeField()
    expires = DateTimeField()

    @property
    def nacl_verifykey(self):
        return VerifyKey(self.key_bytes)

    def bson_verified_loads(self, content: bytes):
        """Returns the decoded bson object if signature is good.
        """
        return bson.decode(self.nacl_verifykey.verify(content))
