'''
Util functions for input handling, transforming etc
'''
import re
from typing import List
from .pydantic_model import Listing
import pandas as pd

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