from flask import Flask
from flask import url_for, request, render_template
from markupsafe import escape

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from datetime import datetime, date

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/<string:name>")
def hello(name=None):
    if request.method == 'POST':
        return 'post request'
    
    return render_template('hello.html', name=name)

@app.route("/name/<string:name>")
def yo_name(name):
    return f'Yo, {escape(name)}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return f'supplied username: {request.form["username"]}'
    return render_template('login.html')


with app.test_request_context():
    print(url_for('yo_name', name='broski'))

# url_for('static', filename='style.css')

@app.route("/plot/<string:term>")
def plot_term(term='python'):
    # img = io.BytesIO()
    sns.set_style("dark")
    sns.color_palette('Spectral')
    df = pd.read_csv("./scraping_results/combined/python/python_2023-11-28.csv", index_col = 0)
    companies = df['company']
    companies = companies.dropna()
    companies_count = companies.value_counts()
    fig = companies_count[:20].plot.pie()

    # y = [1,2,3,4,5]
    # x = [0,2,1,3,4]

    # fig = plt.plot(x,y)

    # plt.savefig(img, format='png')
    today = str(date.today())
    file_name = f'{term}_{today}'
    fig.get_figure().savefig(f'./flask_app/static/images/plots/{file_name}.png')
    
    # plt.close()
    # img.seek(0)

    # plot_url = base64.b64encode(img.getvalue())
    return render_template('plotting.html', plot_name=f'{file_name}.png')
    # return str(os.getcwd())