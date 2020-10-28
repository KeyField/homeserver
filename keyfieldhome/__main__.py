#!/usr/bin/env python3

import argparse
import sys
import os

from . import log, config, app, routes

def __main__():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        type=str,
        help="Config file",
        default="/etc/keyfield/config.toml"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbosity increase"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Verbosity decrease"
    )
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(log.DEBUG)
    if args.quiet:
        log.setLevel(log.WARN)

    if args.config:
        os.environ['KF_HOMESERVER_CONFIG'] = args.config

    app.run()

if __name__ == '__main__':
    __main__()
