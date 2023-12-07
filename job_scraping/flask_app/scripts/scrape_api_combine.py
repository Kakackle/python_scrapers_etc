import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime, date
import pandas as pd
import pickle
import os
import json
from typing import List, Tuple, Callable

"""
Script with functions to scrape data from websites by supplied search_term
coming from calls in endpoints
"""
from .pydantic_model import Listing
from .extractors import extract_careerjet, extract_pracuj, scrape_fluff
from flask import current_app as app
from .path_traversal import reset_path, test_cwd, prepare_folders
from .utils import get_empty_df, get_multiple_terms
from .globals import NUMBER_OF_PAGES

def scrape_websites(search_term: str, urls: List[str], sites: List[str],
                    extractors: List[Callable], folder_path: str) -> pd.DataFrame:
    """
        Scrape through the supplied list of websites using, the supplied extractor functions
        Save each page's result in 'individal' folder in folder_path as csv files
        Combine the results from multiple pages and save in a combined csv file
        Then return a dataframe with the combined results
    Args:
        search_term (List[str]): _description_
        urls (List[str]): _description_
        sites (List[str]): _description_
        extractors (List[function]): _description_
        folder_path (str): _description_

    Returns:
        pd.DataFrame: _description_
    """    
    scraping_results = []
    today = date.today()

    # scrape through all chosen webistes
    for url_index, url in enumerate(urls):
        site_listings = []
        # for a specified number of result pages
        for page in range(1, NUMBER_OF_PAGES+1):
            page_url = url.format(search_term=search_term, page=page)
            page_response = requests.get(page_url)
            page_html = page_response.text
            page_soup = bs(page_html, 'html.parser')
            page_objects = extractors[url_index](page_soup, page)
            site_listings.extend(page_objects)

        # save listings for one site only into a separate file
        site_listings_pd = pd.DataFrame([obj.dict() for obj in site_listings])
        path_ind = folder_path + r'individual'
        if not os.path.exists(path_ind):
            os.makedirs(path_ind)
        path_ind += '/'

        site_listings_pd.to_csv(path_ind + f'{sites[url_index]}_{search_term}_{NUMBER_OF_PAGES}pages_{today}.csv')
        # add to combined multi site results
        scraping_results.extend(site_listings)
    
    print('all listings: ', len(scraping_results))
    
    # save the combined results from all the sites
    sites_string = '_'.join(sites)
    path_comb = folder_path + 'combined'
    if not os.path.exists(path_comb):
        os.makedirs(path_comb)
    path_comb += '/'
    scraping_pd = pd.DataFrame([obj.dict() for obj in scraping_results])
    scraping_pd.to_csv(path_comb + f'{sites_string}_{search_term}_{today}.csv')
    return scraping_pd


def combine_scraping_api(scraping_df: pd.DataFrame,
                        api_df: pd.DataFrame) -> Tuple[pd.DataFrame, tuple[int]]:
    """
    Combine dfs, return result df and shape

    Args:
        scraping_df (_type_): _description_
        api_df (_type_): _description_

    Returns:
        Tuple (_type_): _description_
    """
    result_df = pd.concat([scraping_df, api_df])
    result_shape = result_df.shape
    return result_df, result_shape


def save_combined_results(result_df: pd.DataFrame, folder_path: str,
                          search_term: str):
    today = date.today()
    path = folder_path + r'/all'
    if not os.path.exists(path):
        os.makedirs(path)
    path += '/'
    result_df.to_csv(path + f'all_{search_term}_{str(today)}.csv')


def run_scraping(search_term: str) -> Tuple[pd.DataFrame, Tuple[int]]:
    """_summary_

    Args:
        search_term (_type_): _description_
        urls
        sites
        extractors

    Returns:
        Tuple (_type_): _description_
    """

    urls = [
        'https://www.careerjet.pl/{search_term}-praca.html?radius=0&p={page}&sort=date',
        'https://it.pracuj.pl/praca/{search_term};kw?sc=0&pn={page}'
    ]

    sites = [
        'careerjet',
        'pracuj'
    ]

    extractors = [
        extract_careerjet,
        extract_pracuj
    ]

    today = date.today()
    base_path = reset_path()
    folder_path = prepare_folders(search_term, today, base_path)

    scraping_df = scrape_websites(search_term, urls, sites, extractors,
                    folder_path)
    api_df = scrape_fluff(search_term, folder_path)
    result_df, result_shape = combine_scraping_api(scraping_df, api_df)

    save_combined_results(result_df, folder_path, search_term)
    return result_df, result_shape


def check_if_exists(search_term: str) -> tuple[pd.DataFrame, tuple[int]]:
    """
    Check if result for specified query already exist in saved data
    If they do, choose the latest available data, return a dataframe and it's shape
    If they don't, run scraping functions and return

    Args:
        search_term (str): _description_
        
    Returns:
        Tuple (_type_): _description_
    """

    base_path = reset_path()
    today = date.today()
    
    # FIXME: tutaj chcialbym zeby sprawdzalo czy jest jakikolwiek scrap dla tego terminu i jesli jest to zwracalo najnowszy
    # a nie dokladnie czy jest z dzisiaj
    # i jesli zwraca, to z data z ktorej pochodzi
    # 
    exists_path = base_path + r'/scraping_results/' + search_term

    result_df = get_empty_df()

    # if path exists
    if os.path.exists(exists_path):
        date_folders = os.listdir()
        latest_folder = max(date_folders, key=os.path.getmtime)
        latest_path = os.path.join(exists_path, latest_folder)
        result_df = check_if_all_folder_exists(latest_path)
    
    # if path doesnt exist or was empty, then returned df will be empty, so we have to scrap
    if result_df.empty:
        result_df, result_shape = run_scraping(search_term)

    # if not os.path.exists(exists_path):
        # run scrapers
        
    # or get results from existing ones
    # else:
    #     os.chdir(exists_path)
    #     all_path = exists_path + '/' + 'all'
    #     # check if a combined file exists
    #     if os.path.exists(all_path):
    #         os.chdir(all_path)
    #         files = os.listdir()
    #         for file in files:
    #             if file.endswith('.csv'):
    #                 result_df = pd.read_csv(file, index_col=0)
    #     # combine files
    #     else:
    #         # get the files
    #         paths = [
    #             'combined',
    #             'fluff'
    #         ]
    #         for folder_path in paths:    
    #             try:
    #                 os.chdir(folder_path)
    #                 combined_paths = os.listdir()
    #                 for c_path in combined_paths:
    #                     if c_path.endswith(".csv"):
    #                         combined_df = pd.read_csv(c_path, index_col = 0)
    #                         result_df = pd.concat([result_df, combined_df])
    #             except:
    #                 pass
    #             os.chdir('..')
            
    #         os.chdir('..')
    #     result_shape = result_df.shape

    return result_df, result_shape
    # return_html = f"""
    # <p id="scraping">Resultant scraping shape for {search_term} | {today}: {result_shape}</p>
    # """
    # return return_html


def combine_terms_results(term_list: List[str]):
    terms_string = '_'.join(term_list)
    today = str(date.today())
    results_path = reset_path() + '/scraping_results'
    save_path = results_path + '/' + terms_string + '/' + today + '/'
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path += '/'

    concat_df = get_empty_df()

    for term_folder in os.listdir(results_path):
        if term_folder in term_list:
            # os.chdir(term_folder)
            sub_path = os.path.join(reset_path, term_folder)
            date_folders = os.listdir(term_folder)
            latest_folder = max(date_folders, key=os.path.getmtime)
            sub_path = os.path.join(sub_path, latest_folder)
            
            # new standard - look for a file with results from all apis and websites
            all_path = os.path.join(sub_path, 'all')
            if os.path.exists(all_path):
                for file in os.listdir(sub_path):
                    if file.endswith('.csv'):
                        file_path = os.path.join(sub_path, file)
                        term_df = pd.read_csv(file_path, index_col=0)
                        concat_df = pd.concat([concat_df, term_df])

    # save the new combined df to a file
    concat_df.to_csv(results_path + f'{terms_string}_{today}.csv')
    return concat_df, concat_df.shape

# TODO: funkcja sprawdzajaca czy istneje folder/plik z polaczeniem roznych scrapow
# jesli tak to zwraca o tym informacje i dane o rezultacie znalezionym
# jesli nie to zwraca uzytkownikowi opcje uruchomienia scrapow
# w podstaci przyciskow
def check_if_exists_multiple(term_list: List[str]):
    results = []
    base_path = reset_path()
    today = str(date.today())
    date_regex = re.compile(r'(.*)_(\d{4}-\d{2}-\d{2})')
    terms_string = '_'.join(term_list)

    htmx_plot_action = 'hx-post=/plots/by_file hx-swap=innerHTML hx-target=#plot_multi method=post name=file value='

    result_df = get_empty_df()

    exists_path = base_path + '/scraping_results/' + terms_string
    if os.path.exists(exists_path):
        date_folders = os.listdir(exists_path)
        date_folders =[os.path.join(exists_path, date_folder) for date_folder in date_folders]
        latest_folder = max(date_folders, key=os.path.getmtime)
        for file in os.listdir(latest_folder):
            if file.endswith('.csv'):
                file_path = os.path.join(latest_folder, file)
                # extract the filepath needed for plotting by file function
                # scraping_regex = re.compile('(.*)/scraping_results/(.*)')

                # file_path_after_scraping = scraping_regex.search(file_path).group(2)

                result_df = pd.read_csv(file_path, index_col=0)
                
                regex = date_regex.search(file)

                result_obj = {
                    'term': terms_string,
                    'file': file,
                    'date': regex.group(2),
                    'htmx_action': htmx_plot_action + file,
                    'action_type': 'Plot'
                }
                results.append(result_obj)

    # if result_df.empty:
    for term in term_list:
        result_obj = {
            'term': term,
            'file': '-',
            'date': '-',
            'htmx_action': '',
            'action_type': 'Scrap it'
        }
        term_path = base_path + '/scraping_results/' + term
        if os.path.exists(term_path):
            term_paths = os.listdir(term_path)
            term_paths = [os.path.join(term_path, term) for term in term_paths]
            latest = max(term_paths, key=os.path.getmtime)

            # temporary solution - only checks if folder was found, doesnt look for files

            # result_obj.date = os.path.getmtime(latest)
            # regex = date_regex.search(file)
            # result_obj['date'] = regex.group(2)
            date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
            latest_date = date_regex.match(latest)
            result_obj['date'] = latest
            result_obj['file'] = result_obj['term'] + ' - found'
            # joined = os.path.join(term_path, latest_term_path)
        else:
            result_obj['file']  = result_obj['term'] + ' - not found'
        results.append(result_obj)
    
    return results

# FIXME: funkcja sprawdzajaca czy istnieje folder laczacy rezultaty ze stron i api,
# jesli nie, to tworzy taki i zapisuje dane
# takes a path to the term and date folder combination
def check_if_all_folder_exists(folder_path: str) -> pd.DataFrame:
    base_path = reset_path()
    all_path = folder_path + '/all'

    paths = [
        'combined',
        'fluff'
    ]

    result_df = get_empty_df()

    if os.path.exists(all_path):
        files = os.listdir(all_path)
        for file in files:
            if file.endswith('.csv'):
                result_df = pd.read_csv(file, index_col=0)
    else:
        for sub_path in paths:
            try:
                sub_folder = os.path.join(folder_path, sub_path)
                combined_paths = os.listdir(sub_folder)
                for c_path in combined_paths:
                        if c_path.endswith(".csv"):
                            combined_df = pd.read_csv(c_path, index_col = 0)
                            result_df = pd.concat([result_df, combined_df])
            except:
                pass
        # save the results, important
        os.makedirs(all_path)
        today = str(date.today())
        result_df.to_csv(all_path + '/' + f'all_{today}.csv')
    
    return result_df

