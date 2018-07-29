# -*- coding: utf-8 -*-
"""
File Name：     __init__.py
Author :       peng.he
-------------------------------------------------
"""
import os
import pkgutil
import importlib
from flask import Blueprint
from flask import Flask, jsonify, Response
from functools import wraps
from sentence.logger import init_logger
from sentence.middleware.req_logger import RequestLogger


def route(app, *args, **kwargs):
    """Decorator of flask router."""

    def decorator(f):
        @app.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            sc = 200
            rv = res
            if isinstance(res, Response):
                return res
            if isinstance(res, tuple):
                rv = res[0]
                sc = res[1]
            if isinstance(rv, dict):
                return jsonify(rv), sc
            else:
                return rv, sc

        return wrapper

    return decorator


def app_setting():
    """Get app settings."""
    return os.environ.get(
        'INTELLI_EXTRACT_SENTENCE_PROFILE', 'dev')


def app_config(app):
    """Get app config."""
    testing = app_setting() == 'ci'
    app.config.update(dict(TESTING=testing))


def register_blueprints(app, package_name, package_path):
    """Flask register blueprints helper."""
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


def create_app():
    # initialize logger
    init_logger()

    # initialize app
    app = Flask(__name__)

    # config app
    app_config(app)

    # init request logger
    RequestLogger(app)

    # register bp
    register_blueprints(app, __name__, __path__)
    return app
