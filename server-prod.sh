#!/bin/bash
source ./venv/bin/activate || echo "not using a virtualenv"
export FLASK_ENV=prod
export FLASK_DEBUG=0
echo "server-prod: workdir $PWD"
gunicorn --forwarded-allow-ips='*' "keyfieldhome" -c gunicorn-config.py
