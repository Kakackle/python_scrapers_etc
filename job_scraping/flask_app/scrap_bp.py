from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .scripts.scrape_api_combine import (check_if_exists,
                                         check_if_all_folder_exists,
                                         check_if_exists_multiple)

from .scripts.path_traversal import (test_cwd, reset_path, test_finding)

from .scripts.find_all_scrapes import find_all_scrapes
from .scripts.utils import get_multiple_terms

bp = Blueprint('scrap', __name__, url_prefix='/scrap')

# ---------------------------------------------------------------------------- #
#                                 actual routes                                #
# ---------------------------------------------------------------------------- #

# scrape route
@bp.route("/term_scrap", methods=('POST',))
def term_scrap():
    if request.method == 'POST':
        term = request.form['term'].lower()
        result_df, result_shape = check_if_exists(term)
        # return check_if_exists(term)

# returning / selecting existing scrapes
@bp.route('/prev_scrapes', methods=('GET',))
def prev_scrapes():
    files = find_all_scrapes()
    return render_template('plots/prev_scrapes.html', files = files)

@bp.route('/multi_find', methods=('POST',))
def multi_find():
    if request.method == 'POST':
        terms = request.form['terms']
        terms_split = get_multiple_terms(terms)
        results = check_if_exists_multiple(terms_split)
        return render_template('plots/search_results.html', results=results)


# ---------------------------------------------------------------------------- #
#                                     tests                                    #
# ---------------------------------------------------------------------------- #

@bp.route("/test_cwd", methods=('POST',))
def test_cwd_route():
    if request.method == 'POST':
        return test_cwd()
    
@bp.route("/reset_path", methods=('POST',))
def reset_path_route():
    if request.method == 'POST':
        return reset_path()
    
@bp.route("/test_finding", methods=('POST',))
def test_finding_route():
    if request.method == 'POST':
        return test_finding('python')

@bp.route('/test_multiple', methods=('POST',))
def test_multiple():
    if request.method == 'POST':
        terms = request.form['terms']
        return get_multiple_terms(terms)