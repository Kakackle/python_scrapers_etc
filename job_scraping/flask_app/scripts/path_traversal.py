"""
Path traversal helper scripts
"""
import os
from flask import current_app as app
from datetime import datetime, date
from pathlib import Path


# create folder for scraping results
def prepare_folders(search_term: str, today: date, base_path: str) -> str:
    folder_path = Path(base_path)
    folder_path = folder_path / 'scraping_results' / search_term / str(today)
    # folder_path = base_path + r'/scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # folder_path = folder_path + '/'
    return folder_path

# partial functions

def test_cwd() -> str:
    # starting:
    # C:\Users\User\Desktop\programowanie_web_etc\python_projects\scrapers\job_scraping
    # os.chdir(r'./scraping_results/')
    cur_cwd = str(os.getcwd())
    return_html = f"""
    <p id="scraping_test">{cur_cwd}</p>
    """
    return return_html

def reset_path()-> str:
    root_path = app.root_path
    # instance_path = app.instance_path
    # file_path = os.path.abspath(__file__)
    os.chdir(root_path)
    os.chdir('..')
    cur_cwd = str(os.getcwd())
    return cur_cwd
    # return_html = f"""
    # <p id="scraping_test">{cur_cwd}</p>
    # """


# test if endopoints is able to find files
def test_finding(search_term: str) -> str:
    path = ''
    today = str(date.today())
    test_path = path + r'./scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    # test_path += '/'
    os.chdir(test_path)
    return_html = test_cwd()
    return return_html

def find_file(name: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)