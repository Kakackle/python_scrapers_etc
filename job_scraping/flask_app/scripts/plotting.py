import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import os
import re

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
# TODO: poprzerzucac moze tworzenie poszczegolnych typow plotow do osobnych funkcji
# zeby mozna bylo podac dataframei nazwe kolumny 
# TODO: wyglad - zadne usuwanie whitespace ani nic nie dziala....
def plot_by_file_complete(file: str):
    print('received file name: ', file)
    base_path = reset_path()
    path = os.path.join(base_path, 'scraping_results')
    df_file = find_file(file, path)
    df = pd.read_csv(df_file, index_col=0)

    date_regex = re.compile(r'(.*)_(\d{4}-\d{2}-\d{2})')
    regex = date_regex.search(file)
    terms = regex.group(1)
    terms = terms.split('_')
    terms = ', '.join(terms)
    date_string = regex.group(2)

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
    
    # fig, axes = plt.subplots(2,2, figsize=(20,10))
    fig = plt.figure(figsize=(8,16))
    fig.suptitle(f'Multiple explaratory plots img for [{terms}] - {date_string}')

    # plt.figure(figsize=(20,10))

    # plot skills
    skills_wc = WordCloud(background_color="white", stopwords=STOPWORDS, max_words=50,
                width=800, height=400, collocations=False)
    skills_wordcloud = skills_wc.generate(sum_string)
    skills_ax = fig.add_subplot(3,2,1)
    skills_ax.imshow(skills_wordcloud)
    skills_ax.axis('off')
    skills_ax.set_title("Skills word cloud")

    # skills frequency word pie chart
    words_fc = pd.Series(skills_wc.words_)
    words_fc =  np.ceil(words_fc * len(skills_clean))
    skills_bar_ax = fig.add_subplot(3,2,2)
    skills_bar_fig = words_fc[:20].plot.pie()
    # skills_bar_ax.imshow(skills_bar_fig)
    skills_bar_ax = skills_bar_fig
    skills_bar_ax.set_title('skills frequency bar chart')

    # analyzing job titles / title wordcloud
    title_clean = df['title'].dropna()
    title_string = ' '.join(title_clean.str.lower())
    wc_title = WordCloud(background_color="white", stopwords=STOPWORDS, max_words=50,
                        width=800, height=400)
    title_wordcloud = wc_title.generate(title_string)
    title_ax = fig.add_subplot(3,2,3)
    title_ax.imshow(title_wordcloud)
    title_ax.axis('off')
    title_ax.set_title("Title word cloud")

    # companies pie
    companies = df['company'].value_counts()
    unique_companies = df['company'].unique()
    companies_ax = fig.add_subplot(3,2,4)
    companies_plot_fig = companies[:20].plot.pie()
    companies_ax = companies_plot_fig
    companies_ax.set_title('companies pie chart')

    # desc word cloud
    desc_clean = df['description'].dropna()
    desc_string = ' '.join(desc_clean.str.lower())
    wc_desc = WordCloud(background_color="white", stopwords=STOPWORDS, max_words=50,
                        width=800, height=400)
    desc_wordcloud = wc_desc.generate(desc_string)
    desc_ax = fig.add_subplot(3,2,5)
    desc_ax.imshow(desc_wordcloud)
    desc_ax.axis('off')
    desc_ax.set_title("Desc word cloud")

    # locations
    location_clean = df['location'].dropna()
    location_count_fig = location_clean.value_counts().plot.pie()
    location_ax = fig.add_subplot(3,2,6)
    location_ax = location_count_fig
    location_ax.set_title("Location count")
    
    
    today = str(date.today())
    file_name = f'{file}_wc_{today}'
    fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png',
                             bbox_inches='tight',
                             pad_inches=0.0)
    return file_name