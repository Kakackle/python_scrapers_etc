import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from datetime import datetime
import re
import pandas as pd

search_term = 'seinfeld'

url = f'https://www.olx.pl/oferty/q-{search_term}/'

response = requests.get(url)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

listing_grid = soup.find(class_='listing-grid-container')
# print(len(listing_grid))

listings = listing_grid.find(class_="css-oukcj3")

listings_arr = listings.find_all(class_="css-1sw7q4x")

class Listing(BaseModel):
    title: str
    price: int
    used: bool
    city: str
    date: str
    shipping: bool
    link: str

listings_objects = []

# print(listings_arr[0])
# print('------')
# print(type(listings_arr[0]))

price_regex = re.compile(r'(\d)*')
location_date_regex = re.compile(r'(.*)\s-\s(.*)')

for listing in listings_arr:

    listing_link = listing.find(class_='css-rc5s2u').get('href')
    link = 'olx.pl' + listing_link

    listing_details = listing.find(class_="css-1apmciz")

    listing_title = listing_details.div.h6.getText()
    
    listing_price = int(price_regex.match(listing_details.div.p.getText())[0])
    
    listing_used = listing_details.find(class_="css-112xsl6")

    if listing_used.span:
        listing_used = listing_used.span.span.getText()
    used = False if listing_used == "Nowe" else True

    listing_bottom = listing_details.find(class_="css-veheph").getText()

    bottom_groups = location_date_regex.match(listing_bottom)

    city = bottom_groups[1]
    date = bottom_groups[2]
    
    is_ship = listing.find(class_="css-1xwefxo")
    shipping = True if is_ship else False

    obj = Listing(title=listing_title, price=listing_price,
                  used=used, city=city, date=date, shipping=shipping,
                  link=link)
    listings_objects.append(obj)

# print(*listings_objects[1])
# print(listings_objects[0:3])
listings_pd = pd.DataFrame([obj.dict() for obj in listings_objects])
print(listings_pd.head())

# listings_pd.to_csv(f'{search_term}_pd.csv', index=False)
listings_pd.to_csv(f'{search_term}_pd.csv')