
from . import log, config, routes, db
from .enclave import private_keys

from .app import app

app.before_first_request(config.load)
app.before_first_request(db.connect)
app.before_first_request(private_keys.on_startup)
