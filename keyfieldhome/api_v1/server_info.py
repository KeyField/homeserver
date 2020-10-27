
import msgpack

from ..enclave import private_keys
from .. import config as cfg
from ..utils import make_msgpack_response, sign_response
from .bp import bp

@bp.route('/server/name')
def server_name():
    data = cfg.get('server')['name'].encode('utf-8')
    return sign_response(make_msgpack_response(msgpack.dumps(data)))
