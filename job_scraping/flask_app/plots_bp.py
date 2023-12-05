from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date

bp = Blueprint('plots', __name__)


# generate a new plot by search term
@bp.route("/plot", methods=('POST',))
def plot_term():
    if request.method == 'POST':
        term = request.form['term'].lower()
        sns.set_style("dark")
        sns.color_palette('Spectral')
        df = pd.read_csv("./scraping_results/combined/python/python_2023-11-28.csv", index_col = 0)
        df = df[df['search_term'] == term]
        companies = df['company']
        companies = companies.dropna()
        companies_count = companies.value_counts()
        fig = companies_count[:20].plot.pie()

        today = str(date.today())
        file_name = f'{term}_{today}'
        fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')

        return render_template('plotting.html', plot_name=f'{file_name}.png')
