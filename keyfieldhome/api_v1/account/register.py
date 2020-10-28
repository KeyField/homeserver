
import base64

import msgpack
from flask import request
from nacl.encoding import URLSafeBase64Encoder
from nacl.signing import VerifyKey, SignedMessage

from ... import log
from ...enclave import private_keys, request_decryptor
from ... import config as cfg
from ...models.user import UserProfile, HomeserverUser
from ...models.homeserver import Homeserver
from ...models.public_key import PublicKeyPair
from ...utils import (
    make_msgpack_response,
    sign_response,
    get_decoded_header,
    get_timestamp_seconds,
)
from ..bp import bp

class RegistrationInvalid(ValueError):
    pass

@bp.route('/account/register', methods=['POST'])
def account_register():
    """Attempt to register an account on this homeserver."""
    # the user is most likely undiscovered by this homeserver
    clientsigkey = get_decoded_header('KF-Client-Verify')
    clientsignature = get_decoded_header('KF-Client-Signature')
    # verify the content signature:
    vkey = VerifyKey(clientsigkey)
    req_bytes = vkey.verify(request.data, clientsignature)
    log.info(f"Registration attempt by {vkey.encode(URLSafeBase64Encoder)}")

    msg_signed = private_keys.decrypt_sealed(req_bytes)
    # separate signature from identity block:
    # msg_signed = SignedMessage(msg_bytes)
    msg_bytes = vkey.verify(msg_signed)
    payload = msgpack.unpackb(msg_bytes)

    previous_keys = payload['previous_keys']
    clientverify_urlstr = vkey.encode(URLSafeBase64Encoder).decode()
    main_key_ts = next(k for k,v in previous_keys.items() if v['verify'] == clientverify_urlstr)
    previous_key_times = [k for k,v in previous_keys.items()]
    if (max(previous_key_times) != main_key_ts):
        raise RegistrationInvalid(f"key used for registration must be newest keypair of profile")
    # TODO validate sigchain: to see if a previous key was authorized


    server_user_settings = cfg.get('users')
    if not server_user_settings['public_registration']:
        # TODO: check if public key has been invited / authorized or is in admin_keys
        return 'unauthorized', 401

    # TODO validate username string
    if payload['username'] in server_user_settings['reserved_names']:
        raise RegistrationInvalid(f"username '{payload['username']}' is not available for registration")
    # we don't allow duplicate usernames on the same homeserver:
    if UserProfile.objects(username=payload['username']).count() != 0:
        raise RegistrationInvalid(f"username '{payload['username']}' already taken on this homeserver")
    # only register this user if they declare this homeserver is authoritative:
    declared_verifykey = payload['homeserver']['verify']
    actual_verifykey = private_keys.get_server_verifykey().encode(URLSafeBase64Encoder).decode('utf-8')
    if declared_verifykey != actual_verifykey:
        raise RegistrationInvalid(f"declared homeserver public key {declared_verifykey} does not match this server's key: {actual_verifykey}")
    declared_address = payload['homeserver']['address']
    if declared_address not in cfg.get('server')['external_addresses']:
        raise RegistrationInvalid(f"declared homeserver address {declared_address} is not a valid address of this homeserver")
    # TODO validate signature time within 5 minutes

    # NOTE at this point all checks have passed and we accept the user registration

    # construct a profile of this user:
    new_profile = HomeserverUser(
        username=payload['username'],
        homeserver=Homeserver.objects.get(address=payload['homeserver']['address']),
        current_mainkey=PublicKeyPair(
            verifykey_bytes=clientsigkey,
            publickey_bytes=base64.urlsafe_b64decode(payload['keys']['public']),
            created=main_key_ts,
        ),
        identity_block_signed=msg_signed,
        registered=get_timestamp_seconds(),
    )
    new_profile.save()
    # encrypt the response to them back:
    confirmation = {
        "verify": actual_verifykey, # server's verifykey
        "timestamp": new_profile.registered,
        "identity": new_profile.identity_block_signed,
    }
    packd = msgpack.packb(confirmation)
    # TODO maybe we should encrypt to the device instead of the user?
    resp_box = private_keys.get_user_shared_box(new_profile)
    enc_data = resp_box.encrypt(packd)
    return sign_response(make_msgpack_response(msgpack.dumps(enc_data)))
