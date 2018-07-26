# -*- coding: utf-8 -*-
"""
File Name：     main
Author :       peng.he
-------------------------------------------------
"""
from werkzeug.serving import run_simple
from sentence import api
from sentence import settings


def get_app():
    """Get flask application."""
    app = api.create_app()
    return app


application = get_app()


def main():
    """Run simple server."""
    run_simple(
        settings.IP,
        settings.PORT,
        application,
        use_reloader=False,
        use_debugger=False)
