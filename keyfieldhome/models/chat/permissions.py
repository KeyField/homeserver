
from mongoengine import Document
from mongoengine.fields import *

from ..user import UserProfile


class Role(EmbeddedDocument):
    uuid = UUIDField(required=True)
    order = IntField(required=True)
    grant_scopes = ListField(StringField(min_length=1))
    deny_scopes = ListField(StringField(min_length=1))
    # payload only decryptable by the channel private key: name, color, description, etc
    private_payload = BinaryField()

class PermissionStructure(Document):
    pass # TODO
