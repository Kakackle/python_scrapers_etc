from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

bp = Blueprint('plots', __name__)

@bp.route('/')
def index():
    db = get_db()
    history = db.execute(
        'SELECT h.id, term, action_type, created, author_id, username'
        ' FROM history h JOIN user u ON h.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('plots/index.html', history=history)

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