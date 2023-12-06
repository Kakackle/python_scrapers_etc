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


def run_scraping(search_term: str, urls: List[str], sites: List[str],
                extractors: List[Callable]) -> Tuple[pd.DataFrame, Tuple[int]]:
    """_summary_

    Args:
        search_term (_type_): _description_
        urls
        sites
        extractors

    Returns:
        Tuple (_type_): _description_
    """    
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

    base_path = reset_path()
    today = date.today()
    
    exists_path = base_path + r'/scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(exists_path):
        # run scrapers
        result_df, result_shape = run_scraping(search_term,
                                        urls, sites, extractors)
    # get results from existing ones
    else:
        os.chdir(exists_path)
        all_path = exists_path + '/' + 'all'
        # check if a combined file exists
        if os.path.exists(all_path):
            os.chdir(all_path)
            files = os.listdir()
            for file in files:
                if file.endswith('.csv'):
                    result_df = pd.read_csv(file, index_col=0)
        # combine files
        else:
            # get the files
            paths = [
                'combined',
                'fluff'
            ]
            for folder_path in paths:    
                try:
                    os.chdir(folder_path)
                    combined_paths = os.listdir()
                    for c_path in combined_paths:
                        if c_path.endswith(".csv"):
                            combined_df = pd.read_csv(c_path, index_col = 0)
                            result_df = pd.concat([result_df, combined_df])
                except:
                    pass
                os.chdir('..')
            
            os.chdir('..')
        result_shape = result_df.shape

    return result_df, result_shape
    # return_html = f"""
    # <p id="scraping">Resultant scraping shape for {search_term} | {today}: {result_shape}</p>
    # """
    # return return_html