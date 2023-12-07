import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
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