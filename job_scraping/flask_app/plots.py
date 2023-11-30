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

# index, get user's operation history (scrapes, plots etc)
@bp.route('/')
def index():
    db = get_db()
    history = db.execute(
        'SELECT h.id, term, action_type, created, author_id, username'
        ' FROM history h JOIN user u ON h.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('plots/index.html', history=history)

# generate a new plot by search term

# @bp.route("/plot/<string:term>")
@bp.route("/plot", methods=('POST',))
# def plot_term(term='python'):
def plot_term():
    if request.method == 'POST':
        term = request.form['term'].lower()
        sns.set_style("dark")
        sns.color_palette('Spectral')
        # TODO: tutaj jak dobrze precyzwac czego szukamy
        # po nazwie pliku, folderu czy pozniej
        # po to sa rozne foldery zeby mozna bylo od razu
        # i moze mozna by tez przekazywac dzien z jakiego chcemy
        # albo opcja "wszystkie dni"
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

# CRUD operation for manually creating, updating, deleting history objects

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        term = request.form['term']
        action_type = request.form['action_type']
        error = None

        if not term:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO history (term, action_type, author_id)'
                ' VALUES (?, ?, ?)',
                (term, action_type, g.user['id'])
            )
            db.commit()
            return redirect(url_for('plots.index'))

    return render_template('plots/create.html')

def get_history(id, check_author=True):
    history = get_db().execute(
        'SELECT h.id, term, action_type, created, author_id, username'
        ' FROM history h JOIN user u ON h.author_id = u.id'
        ' WHERE h.id = ?',
        (id,)
    ).fetchone()

    if history is None:
        abort(404, f"History id {id} doesn't exist.")

    if check_author and history['author_id'] != g.user['id']:
        abort(403)

    return history

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    history = get_history(id)

    if request.method == 'POST':
        term = request.form['term']
        action_type = request.form['action_type']
        error = None

        if not term:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE history SET term = ?, action_type = ?'
                ' WHERE id = ?',
                (term, action_type, id)
            )
            db.commit()
            return redirect(url_for('plots.index'))

    return render_template('plots/update.html', history=history)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_history(id)
    db = get_db()
    db.execute('DELETE FROM history WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('plots.index'))