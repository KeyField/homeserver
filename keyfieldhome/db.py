
import mongoengine

from . import config

def connect():
    dbconfig = config.get('db')
    try:
        mongoengine.connect(dbconfig['address'])
    except KeyError as e:
        log.error(f"Failed to connecto to database:")
        log.error(f"{e}")
