from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

bp = Blueprint('index', __name__)

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