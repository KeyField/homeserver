
from mongoengine import Document
from mongoengine.fields import *

from .homeserver import Homeserver
from .user_device import UserDevice
from .public_key import PublicKeyPair
# from .chat.channel import ChatChannel # circular


class UserProfile(Document):
    """Represents a profile of a user.

    This user may or may not be allowed to store on this homeserver,
    see `HomeserverUser` for authorized users.
    """
    meta = {
        "allow_inheritance": True,
    }
    username = StringField(max_length=32, min_length=2, unique=True)
    homeserver = LazyReferenceField(Homeserver, required=True)
    devices = ListField(LazyReferenceField(UserDevice))
    current_mainkey = EmbeddedDocumentField(PublicKeyPair, required=True, unique=True)
    # latest_sigtime = DateTimeField()
    # latest_signed_id_block

    # signed (by user) msgpack'd user identity (profile block)
    signed_identity = BinaryField(required=True)


class HomeserverUser(UserProfile):
    """Represents a user authorized to use this homeserver.
    """
    channels = ListField(LazyReferenceField('ChatChannel', passthrough=True))
    blocked_users = ListField(LazyReferenceField(UserProfile, passthrough=True))
