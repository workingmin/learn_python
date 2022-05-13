#!/usr/bin/env python3

"""
flask run -h 0.0.0.0 -p 5000 --debugger
"""

import os
from flask import Flask
from werkzeug.utils import find_modules, import_string
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler


def register_blueprints(app, pkg='blueprints'):
    for modname in find_modules(pkg):
        mod = import_string(modname)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def create_app(name=__name__):
    app = Flask(name)
    register_blueprints(app)
    
    formatter = Formatter(
        "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s")
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile = os.path.join(logdir, 'app.log')
    handler = TimedRotatingFileHandler(logfile, when="D", encoding="UTF-8")
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
