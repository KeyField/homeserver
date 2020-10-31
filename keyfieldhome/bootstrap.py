
from nacl.encoding import RawEncoder, URLSafeBase64Encoder
import msgpack

from . import config as cfg
from . import log
from .enclave import private_keys
from .models.public_key import PublicKeyPair
from .models.homeserver import Homeserver
from .models.user import UserProfile, HomeserverUser

def on_startup():
    hs_l = ensure_homeserver()

def build_own_profile_block_bytes():
    """The signed identity block for the server"""
    serverconfig = cfg.get('server')
    hs = Homeserver.objects.get(address=serverconfig['external_addresses'][0])
    pb = {
        "username": serverconfig["username"],
        "homeserver": hs.identityblock_homeserver,
        "keys": {
            "verify": private_keys.get_server_verifykey(URLSafeBase64Encoder).decode(),
            "public": private_keys.get_server_publickey(URLSafeBase64Encoder).decode(),
        },
        "previous_keys": {
            "0": { # server keys are permanent
                "verify": private_keys.get_server_verifykey(URLSafeBase64Encoder).decode(),
                "public": private_keys.get_server_publickey(URLSafeBase64Encoder).decode(),
            }
        },
    }
    return private_keys.sign_with_server_key(msgpack.packb(pb))

def ensure_homeserver():
    hs_l = []
    pkp = PublicKeyPair(
        verifykey_bytes=private_keys.get_server_verifykey(RawEncoder),
        publickey_bytes=private_keys.get_server_publickey(RawEncoder),
    )
    serverconfig = cfg.get('server')
    for address in serverconfig['external_addresses']:
        log.debug(f"Verifying local homeserver model for {address}")
        try:
            hs = Homeserver.objects.get(address=address)
            if hs.name != serverconfig['name']:
                log.warn(f"Updating name of homeserver model for address {address} from '{hs.name}' to '{serverconfig['name']}'")
                hs.name = serverconfig['name']
                hs.save()
            if hs.server_username != serverconfig['username']:
                log.warn(f"Updating server username of homeserver model for address {address} from '{hs.server_username}' to '{serverconfig['username']}'")
                hs.server_username = serverconfig['username']
                hs.save()
            if hs.server_key != pkp:
                raise ValueError(f"Local homeserver model for address {address} has incorrect keypair stored.")
            hs_l.append(hs)
        except Homeserver.DoesNotExist as e:
            hs = Homeserver(
                address=address,
                server_key=pkp,
                name=serverconfig["name"],
                server_username=serverconfig['username']
            )
            hs.save()
            hs_l.append(hs)
    # the UserProfile for this server
    try:
        hs_up = UserProfile.objects.get(current_mainkey=pkp)
    except UserProfile.DoesNotExist:
        log.warn(f"Creating UserProfile for homeserver...")
        hs_up = UserProfile(
            username=serverconfig["username"],
            current_mainkey=pkp,
            homeserver=Homeserver.objects.get(address=serverconfig["external_addresses"][0]),
            devices=[],
            identity_block_signed=build_own_profile_block_bytes(),
        )
        hs_up.save()
    return hs_l
