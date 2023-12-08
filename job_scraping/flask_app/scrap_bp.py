from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .scripts.scrape_api_combine import (check_if_exists,
                                         check_if_all_folder_exists,
                                         check_if_exists_multiple,
                                         combine_terms_results,
                                         combine_date_results)

from .scripts.path_traversal import (test_cwd, reset_path, test_finding)

from .scripts.find_all_scrapes import find_all_scrapes
from .scripts.utils import get_multiple_terms

from datetime import datetime, date
import os
import re

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
        return_html = f"""
        <p>resultant df shape: {result_shape}
        """
        return return_html

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

@bp.route('/combine_results', methods=('POST',))
def combine_results():
    if request.method == 'POST':
        terms = request.form['terms_string']
        # terms_split = get_multiple_terms(terms)
        combined_df, combined_shape = combine_terms_results(input_string=terms)
        return_html = f"""
        <p>Resultant combination shape: {combined_shape}</p>
        """
        return return_html
    
# TODO: funcja znajdujaca dokladna kombinacje term i date
# i zwracajaca jesli istneije przyciski plotowania
# a jesli nie znalazlo to informuje o tym
@bp.route('/find_with_date', methods=('POST',))
def find_with_date():
    terms = request.form['terms']
    terms_split = get_multiple_terms(terms)
    terms_string = '_'.join(terms_split)

    search_date = request.form['search_date']

    date_format = r'%Y-%m-%d'
    date_regex = re.compile('.*(\d{4}-\d{2}-\d{2})')
    
    search_date = datetime.strptime(search_date, date_format)

    # get files 
    base_path = reset_path()
    exact_result = ''

    # find a file for the exact combination of terms supplied
    for root, dirs, files in os.walk(base_path):
        for file in files:
            match = date_regex.match(file)
            # jesli szukamy wielu termow
            if '_' in terms_string:
                # znajdz dokladny
                if match and terms_string in file:
                    # results.add(match.group(1))
                    file_date = match.group(1)
                    file_date = datetime.strptime(file_date, date_format)
                    if search_date == file_date:
                        exact_result = file
            else:
                # pojedynczy term, znajdz combined plik zaczynajacy sie od 'all'
                if match and terms_string in file and file.startswith('all'):
                    file_date = match.group(1)
                    file_date = datetime.strptime(file_date, date_format)
                    if search_date == file_date:
                        exact_result = file

    if not exact_result:
        exact_result = 'exact match not found'
        return_html = f"""
        <p>Exact match not found! try a different combination or look at the list</p>
        """
    else:
        return_html = f"""
        <p>Result file: {exact_result}</p>
        <button hx-post=/plots/by_file_complete hx-swap=innerHTML hx-target=#plot_exact method=post name=file value={exact_result}>
        Plot</button>
        """
    return return_html


# TODO: funkcja laczaca rezultaty dla danego term i zakresu dat
# ofc jesli znajdzie
# jesli nie znajdzie nic moze o tym zwrocic informacje uzytkownikowi
# a jesli znajdzie to opcje plotowania itd
# a zeby ulatwic przydaloby sie jeszcze jakos zapisywac do pliku combined
# bo aktualnie mam plot_by_file...
# TODO: dodatkowo fajnie gdyby uzytkownik mogl pobierac taki wygenerowany plik
# zamiast tylko przechowywane na serverze
# czyli sprawdzic temat zwracania przez flask plikow
@bp.route('/combine_from_dates', methods=('POST',))
def combine_from_dates():
    term = request.form['term']
    # terms_split = get_multiple_terms(terms)
    # terms_string = '_'.join(terms_split)

    start_date = request.form['start_date']
    end_date = request.form['end_date']

    date_format = r'%Y-%m-%d'
    date_regex = re.compile('.*(\d{4}-\d{2}-\d{2})')
    
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    # diff = abs((end_date - start_date).days)

    # get files between dates
    base_path = reset_path()
    results = set()
    
    # find files with the term in the date range
    for root, dirs, files in os.walk(base_path):
        for file in files:
            match = date_regex.match(file)
            if match and file.startswith('all') and term in file:
                # results.add(match.group(1))
                file_date = match.group(1)
                file_date = datetime.strptime(file_date, date_format)
                if start_date <= file_date <= end_date:
                    results.add(file)

    # results_string = (', ').join(results)

    if not results:
        return_html = 'files for given combination not found!'
    else:
        result_file = combine_date_results(results)
        res_len = len(results)
        return_html = f"""
        <h3>Combined {res_len} files, would you like to plot the resultant file?</h3>
        <p>{result_file}</p>
        <button hx-post=/plots/by_file_complete hx-swap=innerHTML hx-target=#plot-date-combined method=post name=file value={result_file}>
        Plot</button>
        """
    return return_html
    

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
    
@bp.route('/get_dates', methods=('POST',))
def get_dates():
    if request.method == 'POST':

        terms = request.form['terms']
        terms_split = get_multiple_terms(terms)
        terms_string = '_'.join(terms_split)

        start_date = request.form['start_date']
        end_date = request.form['end_date']

        date_format = r'%Y-%m-%d'
        date_regex = re.compile('.*(\d{4}-\d{2}-\d{2})')
        
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
        # diff = abs((end_date - start_date).days)

        # get files between dates
        base_path = reset_path()
        results = set()
        exact_result = ''

        # find files for scrapes for any of the search terms
        for root, dirs, files in os.walk(base_path):
            for file in files:
                match = date_regex.match(file)
                if match and file.startswith('all'):
                    # results.add(match.group(1))
                    file_date = match.group(1)
                    file_date = datetime.strptime(file_date, date_format)
                    if start_date <= file_date <= end_date:
                        results.add(file)
        
        # find a file for the exact combination of terms supplied
        for root, dirs, files in os.walk(base_path):
            for file in files:
                match = date_regex.match(file)
                if match and terms_string in file:
                    # results.add(match.group(1))
                    file_date = match.group(1)
                    file_date = datetime.strptime(file_date, date_format)
                    if start_date <= file_date <= end_date:
                        exact_result = file

        results_string = (', ').join(results)

        if not exact_result:
            exact_result = 'exact match not found'

        return_html = f"""
        <p>Start: {start_date}</p>
        <p>End: {end_date}</p>
        <p>Results between dates [starting with 'all_']: {results_string}</p>
        <p>Exact match: {exact_result}</p>
        """
        return return_html
    


@bp.route('/get_saved_dates', methods=('GET',))
def get_saved_dates():
    base_path = reset_path()
    date_regex = re.compile('.*(\d{4}-\d{2}-\d{2})')
    date_format = r'%Y-%m-%d'

    results = set()
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            match = date_regex.match(dir)
            if match:
                # results.add(match.group(1))
                results.add(dir)
    # convert string values to dates, sort and back to string 
    results = [datetime.strptime(res, date_format) for res in results]
    results = sorted(results, reverse=True)
    results = [datetime.strftime(res, date_format) for res in results]
    results_string = (', ').join(results)
    return_html = f"""
    <p>{results_string}</p>
    """
    return return_html

                