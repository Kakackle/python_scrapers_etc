from unittest.mock import patch
from datetime import datetime, date

from ..scripts import path_traversal

def test_prepare_folders():
    search_term = 'python'
    today = date.today()
    today_str = str(today)
    base_path = 'test_base'

    result_path = path_traversal.prepare_folders(search_term=search_term,
                                          today=today,
                                          base_path=base_path)
    
    test_path = f"{base_path}/scraping_results/{search_term}/{today_str}/"
    assert result_path == test_path
