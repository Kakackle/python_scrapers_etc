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

from .scripts.plotting import (test_pie_plot, plot_by_file,
                               plot_by_file_complete)

bp = Blueprint('plots', __name__, url_prefix='/plots')

# generate a new plot by search term
@bp.route("/test_plot", methods=('POST',))
def plot_term():
    if request.method == 'POST':
        term = request.form['term'].lower()
        file_name = test_pie_plot(term)

        return render_template('plots/plot_div.html', plot_name=f'{file_name}.png')

@bp.route("/by_file", methods=('POST',))
def plot_file():
    if request.method == 'POST':
        file = request.form['file']
        file_name = plot_by_file(file)
        return render_template('plots/plot_div.html', plot_name=f'{file_name}.png')

@bp.route('/by_file_complete', methods=('POST',))
def plot_complete():
    if request.method == 'POST':
        file = request.form['file']
        file_name = plot_by_file_complete(file)
        return render_template('plots/plot_div.html', plot_name=f'{file_name}.png')