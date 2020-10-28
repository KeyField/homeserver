
from mongoengine import EmbeddedDocument
from mongoengine.fields import *
from nacl.public import PublicKey
from nacl.signing import VerifyKey


class PublicKeyPair(EmbeddedDocument):
    """Represents a PublicKey signed by a VerifyKey.

    Note it's not a direct signing, it's signed into a user identity block.
    The private part can be held by a User or Homeserver.
    """
    verifykey_bytes = BinaryField(required=True)
    publickey_bytes = BinaryField(required=False) # able to be discovered by federation
    created = IntField() # epoch seconds
    expires = IntField() # epoch seconds, NotImplemented / TODO
    # TODO: is successor needed as an EmbeddedDocument ?
    # successor = LazyReferenceField('PublicKeyPair', passthrough=True)

    @property
    def verifykey(self):
        return VerifyKey(self.verifykey_bytes)

    @property
    def publickey(self):
        return PublicKey(self.publickey_bytes)
