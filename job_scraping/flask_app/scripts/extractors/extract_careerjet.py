"""
HTML traversal for and data extraction from careerjet.pl
Compliant to project-wide Listing object data model
Returns a list of Listing objects
"""

from ..pydantic_model import Listing
from typing import List

def extract_careerjet(soup: str, page: int) -> List[Listing]:
    page_objects = []
    try:
        listings = soup.find('ul', attrs={'class': 'jobs'})
        listings_arr = listings.find_all('article', attrs={'class': 'job'})
    except:
        return page_objects
    for listing in listings_arr:
        try:
            listing_link = listing.get('data-url')
            link = f'careerjet.pl{listing_link}'
        except:
            link = ''
            
        try:
            title = listing.header.h2.getText().strip()
        except:
            continue

        try:
            company = listing.find('p', attrs={'class': 'company'}).getText()
        except:
            company = ''

        try:
            location = listing.find('ul', attrs={'class':'location'}).li.getText().strip()
        except:
            location = ''

        try:
            description = listing.find('div', attrs={'class':'desc'}).getText().strip()
        except:
            description = ''
        
        obj = Listing(title = title, link = link, company = company,
                 description = description, location = location)
        page_objects.append(obj)
    print(f'careerjet page {page} objects: ', len(page_objects))
    return page_objects