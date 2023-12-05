from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .scripts.scrape_api_combine import (test_cwd, reset_path,
                                        test_finding, check_if_exists)

from .scripts.find_all_scrapes import find_all_scrapes

bp = Blueprint('scrap', __name__)

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
        
        # basic rendering

        # return render_template('plots/dataframe_basic.html',
        #     tables=[result_df.head().to_html(classes='data')],
        #     titles=result_df.columns.values,
        #     result_shape = result_shape)
    
        # prettier rendering

        return render_template("plots/dataframe_extra.html",
                column_names=result_df.columns.values,
                row_data=list(result_df.head().values.tolist()),
                link_column="title", zip=zip,
                result_shape=result_shape)

# returning / selecting existing scrapes
@bp.route('/prev_scrapes', methods=('GET',))
def prev_scrapes():
    files = find_all_scrapes()
    return render_template('plots/prev_scrapes.html', files = files)

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
        