'''
Util functions for input handling, transforming etc
'''
import re
import os
from typing import List
from .pydantic_model import Listing
import pandas as pd
from datetime import datetime, date

from .path_traversal import reset_path

def get_multiple_terms(text: str) -> List[str]:
    # split by ,
    text_split = text.split(',')
    # remove spaces from within terms
    text_stripped = ["".join(t.split()) for t in text_split]
    return text_stripped

def get_empty_df() -> pd.DataFrame:
    empty_df = pd.DataFrame(columns=['title', 'link', 'company', 'location', 'salary',
                                   'description','date_added', 'skills', 'search_term',
                                   'date_searched'])
    return empty_df

def get_file_dates() -> set[str]:
    """
    Get all dates from saved files

    returns sorted set of dates
    """
    date_format = r'%Y-%m-%d'
    date_regex = re.compile('.*(\d{4}-\d{2}-\d{2})')
    
    base_path = reset_path()

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

    oldest_date = results[-1]
    newest_date = results[0]

    results_string = (', ').join(results)

    return results
