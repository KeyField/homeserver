
import toml
import os
import sys

from . import log

default_config_file = "/etc/keyfield/config.toml"

class KeyFieldHomeServerConfig():
    global_instance = None
    def __init__(self, file):
        self.config_file = toml.load(file)

    def __getitem__(self, name):
        if name in self.config_file:
            return self.config_file[name]
    __getattr__ = __getitem__

def get(name):
    return KeyFieldHomeServerConfig.global_instance[name]

def load(filename: str =default_config_file):
    if os.environ.get('KF_HOMESERVER_CONFIG'):
        filename = os.environ.get('KF_HOMESERVER_CONFIG')
    log.info(f"Loading config file {filename}")
    try:
        with open(filename, 'r') as f:
            KeyFieldHomeServerConfig.global_instance = KeyFieldHomeServerConfig(f)
    except FileNotFoundError as e:
        log.error(f"Could not find config file.")
        log.error(f"{e}")
        sys.exit(2)

    return KeyFieldHomeServerConfig.global_instance
