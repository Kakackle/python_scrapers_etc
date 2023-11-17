import pandas as pd
import os
data_pd = pd.read_csv('./seinfeld_pd.csv', index_col=0)
print(data_pd.head())