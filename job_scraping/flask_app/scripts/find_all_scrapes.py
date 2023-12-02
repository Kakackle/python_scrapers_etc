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
    date_regex = re.compile(r'(.*)(\d{4}-\d{2}-\d{2})')
    dir_objs = []
    base_path = reset_path()
    search_path = base_path + '/scraping_results'
    dirs = os.listdir(search_path)
    # return dirs
    # for dir in dirs:
    #     if dir in ('.ipynb_checkpoints', '_other'):
    #         continue
    #     if dir == 'combined':
    #         combined_dirs = os.listdir('combined')
    #         for comb in combined_dirs:
    #             for file in comb:
    #                 if file.endswith('.csv'):
    #                     result = date_regex.search(file)
    #                     term = result.group(1)
    #                     date = result.group(2)
    #                     dir_objs.append(
    #                         {
    #                             term: term,
    #                             date: date
    #                         }
    #                     )
    #     else:
    #         term_dirs = os.listdir(dir)
    #         for folder in term_dirs:
    #             if folder == '.ipynb_checkbpoints':
    #                 continue
    #             for subfolder in folder:
    #                 if file.endswith('.csv'):
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith('.csv'):
                # print('file', file)
                try:
                    result = date_regex.search(file)
                    term = result.group(1)
                    date = result.group(2)
                    dir_objs.append(
                        {
                            # 'file': file,
                            'term': term,
                            'date': date
                        }
                    )
                except:
                    continue
    # print(dir_objs)
    dir_objs.sort(key = lambda x: x['date'], reverse=True)
    return dir_objs



