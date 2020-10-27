
from nacl.encoding import RawEncoder

from . import config as cfg
from . import log
from .enclave import private_keys
from .models.public_key import PublicKeyPair
from .models.homeserver import Homeserver

def on_startup():
    hs_l = ensure_homeserver()
    up = ensure_profile()

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

def ensure_profile():
    pass
