
from flask import Response, make_response
import nacl
import base64

from . import config as cfg
from . import log
from .enclave import private_keys

class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def set_keyfield_http_headers(r: Response):
    r.headers['KF-Homeserver-Name'] = cfg.get('name')
    r.headers['KF-Homeserver-SigKey'] = private_keys.get_server_verifykey(nacl.encoding.URLSafeBase64Encoder)
    return r

def sign_response(r: Response):
    log.info(f"resp data type: {type(r.data)}")
    signed = private_keys.sign_with_server_key(r.data)
    r.headers['KF-Homeserver-Signature'] = base64.urlsafe_b64encode(signed.signature)
    return r

def make_msgpack_response(*args, **kwargs):
    """Sets the correct mime type / headers, does *not* pack for you."""
    if len(args) == 0:
        raise ValueError("make_msgpack_response needs some content")
    r = make_response(*args, **kwargs)
    r.mimetype = "application/msgpack"
    return r
