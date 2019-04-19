# -*- coding: utf-8 -*-
"""
File Name：     __init__.py
Author :       junjie.zhang
-------------------------------------------------
"""
import os
import pkgutil
import importlib
from flask import Blueprint
from flask import Flask, jsonify, Response
from functools import wraps
from rest.logger import init_logger
from rest.middleware.req_logger import RequestLogger
from rest.api.db import db


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
        'FACE_FUSION', 'dev')


def app_config(app):
    """Get app config."""
    testing = app_setting() == 'ci'
    app.config.update(dict(TESTING=testing))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd())+ os.pathsep+"database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



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

    print("init app")

    # config app
    app_config(app)

    # init request logger
    RequestLogger(app)

    # init database
    with app.app_context(): # 添加这一句，否则会报数据库找不到application和context错误
        db.init_app(app) # 初始化db
        db.create_all() # 创建所有未创建的table

    print("init database")
    print(__name__)
    print(__path__)

    # register bp
    register_blueprints(app, __name__, __path__)
    return app
