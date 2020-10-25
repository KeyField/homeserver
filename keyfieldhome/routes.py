
from flask import make_response

from . import log
from .app import app
from .utils import set_keyfield_http_headers

from . import api_v1

@app.route('/')
def index():
    r = make_response('Hello! This is a KeyField Homeserver.')
    set_keyfield_http_headers(r)
    return r

### API

app.register_blueprint(api_v1.bp, url_prefix='/api/v1')
