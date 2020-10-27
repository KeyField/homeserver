
from mongoengine import Document
from mongoengine.fields import *

# from .user import UserProfile # circular
# from .public_key import PublicKeyPair # device does not have signing key
from ..enclave import private_keys

class UserDevice(Document):
    """Represents a device belonging to a user.
    """
    public_name = StringField(required=True, max_length=256, min_length=1)
    owner = LazyReferenceField('UserProfile', passthrough=True, required=True)
    publickey_bytes = BinaryField(required=True)

    def encrypt_to(content: bytes):
        """Encrypt content from the server to this device."""
        pass
