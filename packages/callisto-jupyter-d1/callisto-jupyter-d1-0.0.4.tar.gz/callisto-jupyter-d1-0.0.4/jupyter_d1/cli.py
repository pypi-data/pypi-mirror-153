#!/usr/bin/env python

import argparse
import os
import sys

import uvicorn  # type: ignore
from uvicorn.config import LOGGING_CONFIG  # type: ignore


def get_args(args):
    desc = "Start Jupyter D1 server"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--port",
        type=int,
        dest="port",
        default=5000,
        help="Port to run jupyter d1 server on",
    )
    parser.add_argument(
        "--secret_token",
        type=str,
        dest="secret_token",
        required=False,
        help="Secret token used to log in to server",
    )
    parser.add_argument(
        "--root_dir",
        type=str,
        dest="root_dir",
        required=False,
        default=None,
        help="Root dir to serve files from",
    )
    parser.add_argument(
        "--log_file",
        type=str,
        dest="log_file",
        required=False,
        default=None,
        help="File to log to",
    )
    parser.add_argument(
        "--log_level",
        type=str,
        dest="log_level",
        required=False,
        default="info",
        help="Log level -- debug/info/warning/error/critical",
    )
    return parser.parse_args(args)


def main(args):
    args = get_args(args)
    os.environ["CALLISTO_ENV"] = "local"
    os.environ["CALLISTO_OAUTH_TOKEN_URL"] = "/login/access-token"
    if args.secret_token is not None:
        os.environ["CALLISTO_LOGIN_TOKEN"] = args.secret_token
    if args.root_dir is not None:
        os.environ["CALLISTO_ROOT_DIR"] = args.root_dir
    log_config = None
    if args.log_file is not None:
        log_config = LOGGING_CONFIG
        log_config["handlers"] = {
            "default": {
                "formatter": "default",
                "class": "logging.FileHandler",
                "filename": args.log_file,
            },
            "access": {
                "formatter": "access",
                "class": "logging.FileHandler",
                "filename": args.log_file,
            },
        }
    protocol = "http"
    host = "127.0.0.1"
    print(f"Jupyter D1 running at {protocol}://{host}:{args.port}")
    uvicorn.run(
        "jupyter_d1:app",
        host=host,
        port=args.port,
        log_level=args.log_level,
        log_config=log_config,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
