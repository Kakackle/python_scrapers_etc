import os
from .scrape_api_combine import reset_path, test_cwd
import re

"""
dir objects
dir_objs = [
    {
        term: 'python',
        date: '2023-11-28'
    },
    {
        term: 'python',
        date: '2023-11-27'
    }
]
"""

def find_all_scrapes():
    date_regex = re.compile(r'(.*)_(\d{4}-\d{2}-\d{2})')
    dir_objs = []
    base_path = reset_path()
    search_path = base_path + '/scraping_results'
    dirs = os.listdir(search_path)
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith('.csv'):
                # print('file', file)
                try:
                    result = date_regex.search(file)
                    term = result.group(1)
                    term_format = (', ').join(term.split('_'))
                    date = result.group(2)
                    dir_objs.append(
                        {
                            'file': file,
                            'term': term_format,
                            'date': date
                        }
                    )
                except:
                    continue
    # print(dir_objs)
    dir_objs.sort(key = lambda x: x['date'], reverse=True)
    return dir_objs



