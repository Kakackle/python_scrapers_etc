from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

bp = Blueprint('index', __name__)

from datetime import datetime, date

from .scripts.utils import get_file_dates

# index, get user's operation history (scrapes, plots etc)
@bp.route('/')
def index():
    db = get_db()
    history = db.execute(
        'SELECT h.id, term, action_type, created, author_id, username'
        ' FROM history h JOIN user u ON h.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    dates = get_file_dates()
    oldest_date = dates[-1]
    newest_date = dates[0]
    today = str(date.today())
    return render_template('index.html', history=history,
                           oldest_date=oldest_date, newest_date=newest_date,
                           today=today)