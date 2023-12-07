import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import os

from .path_traversal import reset_path, find_file

def test_pie_plot(term):
    sns.set_style("dark")
    sns.color_palette('Spectral')
    df = pd.read_csv("./scraping_results/combined/python/python_2023-11-28.csv", index_col = 0)
    # df = pd.read_csv(f"./scraping_results/")
    df = df[df['search_term'] == term]
    companies = df['company']
    companies = companies.dropna()
    companies_count = companies.value_counts()
    fig = companies_count[:20].plot.pie()

    today = str(date.today())
    file_name = f'{term}_{today}'
    fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')
    
    return file_name


def plot_by_file(file):
    base_path = reset_path()
    path = os.path.join(base_path, 'scraping_results')
    df_file = find_file(file, path)
    # return return_file
    df = pd.read_csv(df_file, index_col=0)
    companies = df['company']
    companies = companies.dropna()
    companies_count = companies.value_counts()
    fig = companies_count[:20].plot.pie()

    today = str(date.today())
    file_name = f'{file}_pie_{today}'
    fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')
    return file_name


# make multiple plots instead of a singular company plot
# from file name
def plot_by_file_complete(file: str):
    base_path = reset_path()
    path = os.path.join(base_path, 'scraping_results')
    df_file = find_file(file, path)
    df = pd.read_csv(df_file, index_col=0)

    extra_words = ['']
    stopwords_extra = STOPWORDS.update(['team', 'will', 'looking'])

    # analyzing skills
    skills = df['skills']
    skills_clean = skills.dropna()
    skills_clean = pd.DataFrame(skills_clean, columns=['skills'])
    skills_clean = skills_clean.reset_index(drop=True)

    # Split column cells into separate cells of strings
    skills_string = skills_clean['skills'].str.split(',', expand=True)
    skills_string = skills_string.replace(r'\[', r'', regex=True)
    skills_string = skills_string.replace(r'\]', r'', regex=True)
    skills_string = skills_string.replace(r"'", r'', regex=True)

    skills_string = skills_string.loc[:, :6]
    skills_string.fillna("", inplace=True)
    skills_string.head()

    # Get word count of skills by combining them into a single string (not an array) and using the wordcloud library
    sum_string = ''
    for column in skills_string.columns:
        sum_string += ' '.join(skills_string[column].str.lower())
    
    fig, axes = plt.subplots(2,2, figsize=(20,10))
    fig.suptitle('Multiple explaratory plots img')

    # plt.figure(figsize=(20,10))

    wc = WordCloud(background_color="white", stopwords=STOPWORDS, max_words=50,
                width=800, height=400, collocations=False)
    wordcloud = wc.generate(sum_string)
    fig.add_subplot(wordcloud)
    # todo: wykminic to

    today = str(date.today())
    file_name = f'{file}_wc_{today}'
    fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')
    return file_name