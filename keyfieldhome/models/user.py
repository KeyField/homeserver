
from mongoengine import Document
from mongoengine.fields import *

from .homeserver import Homeserver
from .user_device import UserDevice
from .public_key import PublicKey


class UserProfile(Document):
    """Represents a profile of a user.

    This user may or may not be allowed to store on this homeserver,
    see `HomeserverUser` for authorized users.
    """
    meta = {
        "allow_inheritance": True,
    }
    username = StringField(max_length=32, min_length=2)
    homeserver = LazyReferenceField(Homeserver, required=True)
    devices = ListField(LazyReferenceField(UserDevice))
    current_mainkey = ReferenceField(PublicKey, required=True)


class HomeserverUser(UserProfile):
    """Represents a user authorized to use this homeserver.
    """
    pass
