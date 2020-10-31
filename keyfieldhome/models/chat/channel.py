
from mongoengine import Document
from mongoengine.fields import *

from ..user import UserProfile
from ..homeserver import Homeserver
from .permissions import PermissionStructure, Role


class ChatChannel(Document):
    # NOTE permanent fields:
    uuid = UUIDField(required=True)
    private = BooleanField(required=True, default=True)
    created_time = IntField(required=True)
    created_user = LazyReferenceField(UserProfile, passthrough=True, required=True)
    created_server = LazyReferenceField(Homeserver, passthrough=True, required=True)
    # NOTE mutable fields:
    is_joinable = BooleanField(required=True, default=False)
    # uuid of role to apply to members who add themselves:
    join_role = UUIDField(required=False)
    # users who can modify any of the channel's mutable fields:
    owners = ListField(LazyReferenceField(UserProfile, passthrough=True), required=True)
    # any access from these users to this channel's resources is blocked
    banned = ListField(LazyReferenceField(UserProfile, passthrough=True))
    # reader_event_types = ListField(StringField(min_length=1), default=[])
    # writer_event_types = ListField(StringField(min_length=1), default=['io.keyfield.chat.*'])
