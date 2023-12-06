'''
Util functions for input handling, transforming etc
'''
import re
from typing import List

def get_multiple_terms(text: str) -> List[str]:
    # split by ,
    text_split = text.split(',')
    # remove spaces from within terms
    text_stripped = ["".join(t.split()) for t in text_split]
    return text_stripped