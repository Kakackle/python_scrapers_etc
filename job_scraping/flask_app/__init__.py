from flask import Flask
from flask import url_for, request, render_template
from markupsafe import escape
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from datetime import datetime, date

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'scraping.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import plots_bp
    app.register_blueprint(plots_bp.bp)

    from . import scrap_bp
    app.register_blueprint(scrap_bp.bp)

    from . import history_bp
    app.register_blueprint(history_bp.bp)

    from . import index_bp
    app.register_blueprint(index_bp.bp)

    app.add_url_rule('/', endpoint='index')
    # app.add_url_rule('/', endpoint='index')

    return app