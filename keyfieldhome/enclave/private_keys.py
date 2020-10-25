
from mongoengine import Document
from mongoengine.fields import *
import nacl
from nacl.public import PrivateKey, Box
from nacl.signing import SigningKey, VerifyKey

from .. import log
from .. import config as cfg
from ..models.encryption_key import PublicEncryptionKey

class PrivateServerKey(Document):
    """Private signing key of the server.
    """
    meta = {'collection':'server_private'}
    username = StringField(required=True)
    private_key_bytes = BinaryField(required=True)

def _get_server_username():
    return cfg.get('server')['username']

def _get_server_signingkey():
    psk = PrivateServerKey.objects.get(username=_get_server_username())
    return SigningKey(psk.private_key_bytes)

def _get_server_privatekey():
    psk = _get_server_signingkey()
    return psk.to_curve25519_private_key()

def get_server_verifykey(encoder=nacl.encoding.RawEncoder):
    return _get_server_signingkey().verify_key.encode(encoder)

def get_server_publickey(encoder=nacl.encoding.RawEncoder):
    return _get_server_privatekey().public_key.encode(encoder)

def on_startup():
    # verification / initialization checks
    if PrivateServerKey.objects(username=_get_server_username()).first() == None:
        log.warn(f"No server account key found in database for '{_get_server_username()}'")
        log.warn(f"Generating new keypair, if this is unexpected please check your database.")

        sk = SigningKey.generate()
        psk = PrivateServerKey(username=_get_server_username(), private_key_bytes=sk.encode())
        psk.save()
    # log.info(f"Server public key ")

def sign_with_server_key(content: bytes):
    signkey = _get_server_signingkey()
    sc = signkey.sign(content)
    return sc
