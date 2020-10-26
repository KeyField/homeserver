
from mongoengine import Document
from mongoengine.fields import *

from ..user import UserProfile
from ..homeserver import Homeserver


class ChatChannel(Document):
    # permanent fields:
    private = BooleanField(required=True, default=True)
    created_time = DateTimeField(required=True)
    created_user = LazyReferenceField(UserProfile, passthrough=True, required=True)
    created_server = LazyReferenceField(Homeserver, passthrough=True, required=True)
    # mutable fields:
    owners = ListField(LazyReferenceField(UserProfile, passthrough=True), required=True)
    writers = ListField(LazyReferenceField(UserProfile, passthrough=True))
    readers = ListField(LazyReferenceField(UserProfile, passthrough=True))
    banned = ListField(LazyReferenceField(UserProfile, passthrough=True))
    is_joinable = BooleanField(required=True, default=False)
    join_role = StringField(choices=('owners', 'writers', 'readers'))
