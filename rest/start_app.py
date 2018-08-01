# -*- coding: utf-8 -*-
"""
File Name：     main
Author :       peng.he
-------------------------------------------------
"""
from werkzeug.serving import run_simple
from rest import api
from rest import settings


def get_app():
    """Get flask application."""
    app = api.create_app()
    return app


application = get_app()
print("d")


def main():
    """Run simple server."""
    run_simple(
        settings.IP,
        settings.PORT,
        application,
        use_reloader=False,
        use_debugger=False)
main()
