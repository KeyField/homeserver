
import msgpack

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response, bytes_from_urlstr
from ..models.public_key import PublicKeyPair
from ..models.user import UserProfile
from .bp import bp

@bp.route('/profile/<keyid>')
def get_profile(keyid):
    """Lookup a user identity block by key ID."""
    fedconfig = cfg.get("federation")

    if fedconfig['public_profiles'] is False:
        # only users of this homeserver are allowed to retrieve identities
        pass # TODO

    if fedconfig['auto_update_nonlocal_profiles']:
        # attempt to pull newer information from that profile's homeserver first
        pass # TODO

    verifykey_bytes = bytes_from_urlstr(keyid)
    try:
        userprofile = UserProfile.objects.get(current_mainkey__verifykey_bytes=verifykey_bytes)
    except UserProfile.DoesNotExist as e:
        return 'not found', 404

    return sign_response(make_msgpack_response(userprofile.identity_block_signed))
