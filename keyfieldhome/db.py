
import mongoengine

from . import config

def connect():
    dbconfig = config.get('db')
    try:
        mongoengine.connect(dbconfig['database_name'], host=dbconfig['address'], port=dbconfig.get('port'))
    except KeyError as e:
        log.error(f"Failed to connecto to database:")
        log.error(f"{e}")
