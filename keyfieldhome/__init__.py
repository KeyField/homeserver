
from . import log, config, routes, db, bootstrap
from .enclave import private_keys
from .app import app

app.before_first_request(config.load)
app.before_first_request(db.connect)
app.before_first_request(private_keys.on_startup)

app.before_first_request(bootstrap.on_startup)

__version__ = "0.0.1"

application = app
