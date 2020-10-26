
import msgpack

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response, key_from_urlstr, key_to_urlstr
from ..models.public_key import PublicKey
from .bp import bp

@bp.route('/profile/<keyid>')
def get_profile(keyid):
    key_bytes =
    pkey = PublicKey.objects.get()
    return sign_response(make_msgpack_response(msgpack.dumps(data)))
