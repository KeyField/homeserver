
from mongoengine import Document
from mongoengine.fields import *

# from .user import UserProfile # circular
from .public_key import PublicKey
from .encryption_key import PublicEncryptionKey

class UserDevice(Document):
    """Represents a device belonging to a user.
    """
    public_name = StringField(required=True, max_length=1024, min_length=1)
    owner = LazyReferenceField('UserProfile', passthrough=True, required=True)
    public_key = LazyReferenceField(PublicKey, passthrough=True, required=True)
    encryption_key = LazyReferenceField(PublicEncryptionKey, passthrough=True, required=True)
