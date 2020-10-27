
from flask import Request
import nacl
from nacl.public import PrivateKey, Box
from nacl.signing import VerifyKey

from ..utils import get_decoded_header
from . import private_keys

def load_client_request_data(req: Request):
    clientsigkey = get_decoded_header('KF-Client-SigKey')
    clientsignature = get_decoded_header('KF-Client-Signature')
    # TODO
