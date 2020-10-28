
import msgpack
from nacl.encoding import URLSafeBase64Encoder

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response, get_timestamp_seconds
from .bp import bp

@bp.route('/server/name')
def server_name():
    data = cfg.get('server')['name'].encode('utf-8')
    return sign_response(make_msgpack_response(msgpack.dumps(data)))

@bp.route('/server/publickey')
def server_publickey():
    serverconfig = cfg.get('server')
    data = {
        "name": serverconfig["name"],
        "public": private_keys.get_server_publickey(URLSafeBase64Encoder).decode(),
        "timestamp": get_timestamp_seconds(),
    }
    return sign_response(make_msgpack_response(msgpack.dumps(data)))
