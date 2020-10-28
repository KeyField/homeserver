
from keyfieldhome import log as log

reload = True
pidfile = "/tmp/keyfield_homeserver.pid"
bind = ['unix:/tmp/keyfield_homeserver.sock', '0.0.0.0:8008']
# worker_class = "gthread"
workers = 8

def on_reload(server):
    log.info("gunicorn reload")

def when_ready(server):
    log.info("gunicorn ready")

def on_exit(server):
    log.info("gunicorn exit")
