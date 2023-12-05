"""
HTML traversal for and data extraction from careerjet.pl
Compliant to project-wide Listing object data model
Returns a list of Listing objects,
"""

from ..pydantic_model import Listing
import re
from typing import List

# regexes
pracuj_date = re.compile(r'Opublikowana: (.*)')

def extract_pracuj(soup: str, page: int) -> List[Listing]:
    page_objects = []
    try:
        listings = soup.find('div', attrs={'data-test': 'section-offers'})
        listings_arr = listings.find_all(class_='c1fljezf')
    except:
        return page_objects
    
    for listing in listings_arr:
        try:
            listing_link = listing.find('a', attrs={'data-test': 'link-offer'}).get('href')
        except:
            listing_link = ''
        
        try:
            listing_title = listing.find('h2', attrs={'data-test': 'offer-title'}).a.getText()
        except:
            listing_title = ''
    
        try:
            listing_date = listing.find('p', attrs={'data-test':'text-added'}).getText()
            listing_date = pracuj_date.match(listing_date)[0]
        except:
            listing_date = ''
    
        try:
            listing_skills = []
            skills = listing.find_all('span', attrs={'data-test': 'technologies-item'})
            for skill in skills:
                skill = skill.getText()
                listing_skills.append(skill)
        except:
            listing_skills = []
    
        try:
            listing_company = listing.find('a', attrs={'data-test':'text-company-name'}).getText()
        except:
            listing_company = ''
    
        try:
            listing_location = listing.find('h5', attrs={'data-test':'text-regon'}).getText()
        except:
            listing_location = ''
    
        try:
            listing_description = listing.find('span', attrs={'class':'t126uk2l'}).getText()
        except:
            listing_description = ''
    
        try:
            listing_salary = listing.find('span', attrs={'data-test':'offer-salary'}).getText()
        except:
            listing_salary = ''
            
        obj = Listing(title = listing_title, link = listing_link,
                      date_added = listing_date, skills = listing_skills,
                     company = listing_company, location = listing_location,
                     description = listing_description, salary  = listing_salary)
        page_objects.append(obj)
        
    print(f'pracuj.pl page {page} objects: ', len(page_objects))
    return page_objects