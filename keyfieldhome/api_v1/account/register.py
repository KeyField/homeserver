
import msgpack
from flask import request
from nacl.encoding import URLSafeBase64Encoder
from nacl.signing import VerifyKey

from ... import log
from ...enclave import private_keys, request_decryptor
from ... import config as cfg
from ...models.user import UserProfile
from ...utils import make_msgpack_response, sign_response, get_decoded_header
from ..bp import bp

class RegistrationInvalid(ValueError):
    pass

@bp.route('/account/register', methods=['POST'])
def account_register():
    """Attempt to register an account on this homeserver."""
    # the user is most likely undiscovered by this homeserver
    clientsigkey = get_decoded_header('KF-Client-SigKey')
    clientsignature = get_decoded_header('KF-Client-Signature')
    # verify the content signature:
    vkey = VerifyKey(clientsigkey)
    req_bytes = vkey.verify(request.data, clientsignature)
    log.info(f"Registration attempt by {vkey.encode(URLSafeBase64Encoder)}")

    server_user_settings = cfg.get('users')
    if not server_user_settings['public_registration']:
        # TODO: check if public key has been invited / authorized or is in admin_keys
        return 'unauthorized', 401

    msg_bytes = private_keys.decrypt_sealed(req_bytes)

    payload = msgpack.unpackb(
        msg_bytes,
        max_buffer_size=10*1024*1024, # 10MB
    )
    # TODO validate username string
    # we don't allow duplicate usernames on the same homeserver:
    if UserProfile.objects(username=payload['username']).count() != 0:
        raise RegistrationInvalid(f"username '{payload['username']}' already taken on this homeserver")
    # only register this user if they declare this homeserver is authoritative:
    if payload['homeserver']['public'] != private_keys.get_server_publickey().encode(URLSafeBase64Encoder).decode('utf-8'):
        raise RegistrationInvalid(f"declared homeserver public key does not match")
    if payload['homeserver']['address'] not in cfg.get('server')['external_addresses']:
        raise RegistrationInvalid(f"declared homeserver address is not a valid address of this homeserver")
    # TODO validate signature time within 5 minutes
    # TODO validate sigchain
    # construct a profile of this user:
    new_profile = UserProfile(
        # TODO
    )


    return sign_response(make_msgpack_response(msgpack.dumps(data)))
