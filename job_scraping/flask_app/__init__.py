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

    # url_for('static', filename='style.css')

    @app.route("/plot/<string:term>")
    def plot_term(term='python'):
        # img = io.BytesIO()
        sns.set_style("dark")
        sns.color_palette('Spectral')
        df = pd.read_csv("./scraping_results/combined/python/python_2023-11-28.csv", index_col = 0)
        companies = df['company']
        companies = companies.dropna()
        companies_count = companies.value_counts()
        fig = companies_count[:20].plot.pie()

        # y = [1,2,3,4,5]
        # x = [0,2,1,3,4]

        # fig = plt.plot(x,y)

        # plt.savefig(img, format='png')
        today = str(date.today())
        file_name = f'{term}_{today}'
        fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')
        
        # plt.close()
        # img.seek(0)

        # plot_url = base64.b64encode(img.getvalue())
        return render_template('plotting.html', plot_name=f'{file_name}.png')
        # return str(os.getcwd())
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import plots
    app.register_blueprint(plots.bp)
    app.add_url_rule('/', endpoint='index')

    return app