import requests
from bs4 import BeautifulSoup
url = 'https://www.olx.pl/oferty/q-seinfeld/'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
listing_grid = soup.find(class_='listing-grid-container')
listings = listing_grid.find(class_="css-oukcj3")
listings_arr = listings.find_all(class_="css-1sw7q4x")
listing = listings_arr[0]
listing_details = listing.find(class_="css-1apmciz")
# listing_price = listing_details.div.p.span.getText()
listing_link = listing.find(class_="css-rc5s2u").get('href')
print(listing_link)
