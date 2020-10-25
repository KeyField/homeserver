
from flask import Flask
from . import log

app = Flask("KeyFieldHomeserver")

if app.debug:
    log.setLevel(log.DEBUG)
    log.debug("Logging set to debug by flask app debug.")
