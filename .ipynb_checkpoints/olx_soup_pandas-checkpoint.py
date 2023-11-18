import pandas as pd
import matplotlib.pyplot as plt
import os
data_pd_raw = pd.read_csv('./seinfeld_pd.csv', index_col=0)
data_pd_raw.dropna()
# print(f'columns: {data_pd_raw.columns}')
# filtering non-seinfeld related
# non_sein = data_pd.loc[~data_pd['title'].str.contains('seinfeld', case=False)]
data_pd = data_pd_raw.loc[data_pd_raw['title'].str.contains('seinfeld', case=False)]

# 3 categories we're interested in
lego_rows = data_pd.loc[data_pd['title'].str.contains('lego', case=False)]
funko_rows = data_pd.loc[data_pd['title'].str.contains('funko', case=False)]
dvd_rows = data_pd.loc[data_pd['title'].str.contains('dvd', case=False)]

# explore lego prices spread

lego_prices = lego_rows['price']
lego_prices_hist = lego_prices.hist()
# print(lego_prices.describe())
# plt.show()

# cut off low prices, filter by city or with shipping

my_city = 'łódź'

filtered_lego = lego_rows.loc[lego_rows['price'].gt(100)
                                & ( lego_rows['city'].str.contains(my_city, case=False)
                                   | lego_rows['shipping'] == True
                                   )]
# print('filtered lego')
# print(filtered_lego.describe())
filtered_new = filtered_lego.loc[filtered_lego['used'] == False]
filtered_used = filtered_lego.loc[filtered_lego['used'] == True]
# print(filtered_new.count())
# print(filtered_used.count())
# print(filtered_lego.loc[filtered_lego['city'].str.contains(my_city, case=False)].any())
min_filtered_price = filtered_new[filtered_new['price'] == filtered_new['price'].max()]
print(min_filtered_price)