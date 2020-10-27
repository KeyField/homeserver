
import msgpack

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response
from ..models.public_key import PublicKeyPair
from .bp import bp

@bp.route('/profile/<keyid>')
def get_profile(keyid):
    pass
