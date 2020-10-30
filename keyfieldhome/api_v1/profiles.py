
import msgpack

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response, bytes_from_urlstr
from ..models.public_key import PublicKeyPair
from ..models.user import UserProfile
from .bp import bp

@bp.route('/profile/<keyid>')
def get_profile(keyid):
    """Unauthenticated route, information is public, so no encryption."""
    verifykey_bytes = bytes_from_urlstr(keyid)

    try:
        userprofile = UserProfile.objects.get(current_mainkey__verifykey_bytes=verifykey_bytes)
    except UserProfile.DoesNotExist as e:
        return 'not found', 404

    return sign_response(make_msgpack_response(userprofile.identity_block_signed))
