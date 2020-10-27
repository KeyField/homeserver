
from .. import log
from ..utils import set_keyfield_http_headers

from . import server_info, profiles
from .account import register

from .bp import bp

bp.after_request(set_keyfield_http_headers)

__all__ = [
    bp
]
