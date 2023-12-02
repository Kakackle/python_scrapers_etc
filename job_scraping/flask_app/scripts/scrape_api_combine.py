import requests
from bs4 import BeautifulSoup as bs
import re
from datetime import datetime, date
import pandas as pd
import pickle
import os
import json

from .pydantic_model import Listing

from flask import current_app as app

# ---------------------------------------------------------------------------- #
#                             scraping preparation                             #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                             extraction functions                             #
# ---------------------------------------------------------------------------- #

# regexes
pracuj_date = re.compile(r'Opublikowana: (.*)')

def extract_careerjet(soup, page):
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

def extract_pracuj(soup, page):
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



# ---------------------------------------------------------------------------- #
#                      preparing folders to save data into                     #
# ---------------------------------------------------------------------------- #

# FIXME: put this into a function receiving search_term

def prepare_folders(search_term, today, base_path):

    folder_path = r'./scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = folder_path + '/'
    return folder_path

def scrape_websites(search_term, today, urls, sites, extractors,
                     path, no_pages, scraping_results):
    # proxies = {'https:' :'http://127.0.0.1:5000'}
    # proxies = {
    # 'http': 'http://127.0.0.1:8888',
    # 'https': 'http://127.0.0.1:8888',
    # }
    page = 1
    for url_index, url in enumerate(urls):
        site_listings = []
        for page in range(1,no_pages+1):
            page_url = url.format(search_term=search_term, page=page)
            # page_response = requests.get(page_url, proxies=proxies, verify=False)
            page_response = requests.get(page_url)
            page_html = page_response.text
            page_soup = bs(page_html, 'html.parser')
            page_objects = extractors[url_index](page_soup, page)
            site_listings.extend(page_objects)
        # save listings for one site only
        site_listings_pd = pd.DataFrame([obj.dict() for obj in site_listings])
        path_ind = path + r'individual'
        if not os.path.exists(path_ind):
            os.makedirs(path_ind)
        path_ind += '/'
        site_listings_pd.to_csv(path_ind + f'{sites[url_index]}_{search_term}_{no_pages}pages_{today}.csv')
        # add to combined multi site results
        scraping_results.extend(site_listings)
    print('all listings: ', len(scraping_results))
    # save the combined results from sites
    sites_string = '_'.join(sites)
    path_comb = path + 'combined'
    if not os.path.exists(path_comb):
        os.makedirs(path_comb)
    path_comb += '/'
    scraping_pd = pd.DataFrame([obj.dict() for obj in scraping_results])
    scraping_pd.to_csv(path_comb + f'{sites_string}_{search_term}_{today}.csv')
    return scraping_pd
# ---------------------------------------------------------------------------- #
#                             fluff api preparation                            #
# ---------------------------------------------------------------------------- #

def scrape_fluff(search_term, today, path, no_pages, api_results):

    url = "https://nofluffjobs.com/api/search/posting?page=1&limit=50&salaryCurrency=PLN&salaryPeriod=month&region=pl"

    headers = {
    'authority': 'nofluffjobs.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/postingSearch+json',
    'cookie': 'nfj_visited_pl=true; lastSearches=true; OptanonAlertBoxClosed=2023-11-02T15:26:46.991Z; nfj_abt=cat3422%2C0%2C1%3Bldm4333%2C0%2C0%3Bpagesize%2C0%2C0; nfj_redirect_id=00d16475-3c5d-45f3-8ea1-0d8115160a5f; postingApplied_UC5ICGL1=true; nfj_policy_accepted=true; nfj_consents={%22consent_initialized%22:true%2C%22consent_analytics_storage%22:false%2C%22consent_ad_storage%22:false%2C%22consent_functionality_storage%22:false%2C%22onetrust_consent_id%22:%221fb66390-249c-4825-8551-d857cf557193%22%2C%22onetrust_geolocation%22:%22PL%22%2C%22consent_analytics_storage_date%22:%222023-10-25T09:47:48.968Z%22%2C%22consent_functionality_storage_date%22:%222023-10-25T09:47:48.968Z%22%2C%22consent_ad_storage_date%22:%222023-10-25T09:47:48.968Z%22%2C%22first_consent_selection%22:true%2C%22consent_selection_date%22:%222023-10-25T09:47:48.968Z%22}; AMP_MKTG_53ff6cd964=JTdCJTdE; nfj_new_user=true; nfj_session_id=88499a3d-5615-48ca-9bb0-69fd8a9c1fd4.1700752947104; _dcid=88499a3d-5615-48ca-9bb0-69fd8a9c1fd4; nfj_selected_region=PL; country_iso=US; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+23+2023+16%3A23%3A59+GMT%2B0100+(Central+European+Standard+Time)&version=202310.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1fb66390-249c-4825-8551-d857cf557193&interactionCount=2&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=PL%3B10; AMP_53ff6cd964=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI4ODQ5OWEzZC01NjE1LTQ4Y2EtOWJiMC02OWZkOGE5YzFmZDQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzAwNzUyOTQ3MTA0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlN0Q=; nfj_last=1700753048139; _dd_s=rum=2&id=7cc82860-2c42-40c2-b559-11a3c23d0017&created=1700752947384&expire=1700753949314',
    'nfj-global-context': '{"region":"PL","lang":"pl","global_is_employer_logged_in":false,"global_is_candidate_logged_in":false,"global_internal_traffic":false,"global_partnerId":null,"global_partnerInternalTraffic":false,"global_url":"https://nofluffjobs.com/pl/Python?page=1","global_windowResolution":"649x919","global_pixelRatio":1,"global_screenWidth":1920,"global_screenHeight":1040,"global_deviceCategory":"desktop","global_deviceFamily":"Windows","global_userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36","global_company_domain":null}',
    'origin': 'https://nofluffjobs.com',
    'pragma': 'no-cache',
    'referer': 'https://nofluffjobs.com/pl/Python?page=1',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-datadog-origin': 'rum',
    'x-datadog-parent-id': '8273576369410968673',
    'x-datadog-sampling-priority': '1',
    'x-datadog-trace-id': '776451047921066142'
    }

    search_tech = search_term.capitalize()

    raw_search = f"requirement={search_tech}"

    payload = json.dumps({
    "rawSearch": raw_search
    })

    # postings_half = []
    for page in range(1, no_pages):
        page_url = f"https://nofluffjobs.com/api/search/posting?page={page}&limit=50&salaryCurrency=PLN&salaryPeriod=month&region=pl"
        page_r = requests.request("POST", page_url, headers=headers, data=payload)
        page_data = page_r.json()
        page_postings = page_data['postings']
        for post in page_postings:
            api_results.append(post)
        print('page postings: ',len(page_postings))
    print('postings half: ', len(api_results))

    api_df = pd.json_normalize(api_results)

    # ---------------------------------------------------------------------------- #
    #                             data transformations                             #
    # ---------------------------------------------------------------------------- #

    df = api_df
    df['salary'] = df['salary.from'].astype(str) + ' - ' + df['salary.to'].astype(str)

    # Create new conforming dataframe
    # add empty columns where not present in data
    # convert dates

    listing_df = df[['title', 'url', 'name', 'salary', 'posted', 'technology']]
    listing_df.rename(columns={'url':'link', 'name':'company',
                            'technology':'skills', 
                            'posted':'date_added'}, inplace=True)
    # listing_df.columns.get_loc('company')
    listing_df.insert(listing_df.columns.get_loc('company')+1, 'location', '')
    listing_df.insert(listing_df.columns.get_loc('salary')+1, 'description', '')
    listing_df.insert(listing_df.columns.get_loc('skills')+1, 'search_term', search_tech.lower())
    listing_df.insert(listing_df.columns.get_loc('search_term')+1, 'date_searched', date.today())
    listing_df['date_added'] = listing_df['date_added'].apply(lambda x: datetime.fromtimestamp(x/1000).date())
    # listing_df['date_added'] = datetime.fromtimestamp(listing_df['date_added']/1000).date()
    # listing_df.head()

    # save results
    path = r'./scraping_results' + '/' + search_term + '/' + str(today) + r'/nofluff'
    if not os.path.exists(path):
        os.makedirs(path)
    path += '/'
    listing_df.to_csv(path + f'nofluff_{search_term}_{today}.csv')
    
    api_df = listing_df
    return api_df
    
def combine_scraping_api(scraping_df, api_df):
    result_df = pd.concat([scraping_df, api_df])
    result_shape = result_df.shape
    return result_df, result_shape

def save_combined_results(result_df, base_path, search_term, today):
    path = base_path + r'/scraping_results' + '/' + search_term + '/' + str(today) + r'/all'
    if not os.path.exists(path):
        os.makedirs(path)
    path += '/'
    result_df.to_csv(path + f'all_{search_term}_{str(today)}.csv')

def run_scraping(search_term, today, pages, urls, sites, extractors,
                scraping_results, scraping_df,
                api_results, api_df):
    base_path = reset_path()
    folder_path = prepare_folders(search_term, today, base_path)
    scraping_df = scrape_websites(search_term, today, urls, sites, extractors,
                    folder_path, pages, scraping_results)
    api_df = scrape_fluff(search_term, today, folder_path, pages, api_results)
    result_df, result_shape = combine_scraping_api(scraping_df, api_df)
    save_combined_results(result_df, base_path, search_term, today)
    return result_df, result_shape

# function to check if scraping results already exist
def check_if_exists(search_term):
    no_pages = 2 # number of pages to look through when sraping and getting from the apis
    today = date.today()

    scraping_results = []
    scraping_df = pd.DataFrame()
    api_results = []
    api_df = pd.DataFrame()

    result_df = pd.DataFrame()
    result_shape = None

    urls = [
        'https://www.careerjet.pl/{search_term}-praca.html?radius=0&p={page}&sort=date',
        'https://it.pracuj.pl/praca/{search_term};kw?sc=0&pn={page}'
    ]

    sites = [
        'careerjet',
        'pracuj'
    ]

    extractors = [
        extract_careerjet,
        extract_pracuj
    ]

    base_path = reset_path()
    exists_path = base_path + r'/scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(exists_path):
        # run scrapers
        result_df, result_shape = run_scraping(search_term, today, no_pages,
                                                urls, sites, extractors,
                     scraping_results, scraping_df, api_results, api_df)
    else:
        os.chdir(exists_path)
        all_path = exists_path + '/' + 'all'
        # check if a comind file exists
        if os.path.exists(all_path):
            os.chdir(all_path)
            files = os.listdir()
            for file in files:
                if file.endswith('.csv'):
                    result_df = pd.read_csv(file, index_col=0)
        # combine files
        else:
            # get the files
            paths = [
                'combined',
                'fluff'
            ]
            try:
                os.chdir('combined')
                combined_paths = os.listdir()
                for c_path in combined_paths:
                    if c_path.endswith(".csv"):
                        combined_df = pd.read_csv(c_path, index_col = 0)
                        # print(f"shape: {combined_df.shape}")
                        result_df = pd.concat([result_df, combined_df])
            except:
                pass
            os.chdir('..')
            try:
                os.chdir('nofluff')
                combined_paths = os.listdir()
                for c_path in combined_paths:
                    # print(f"c_path: {c_path}")
                    if c_path.endswith(".csv"):
                        combined_df = pd.read_csv(c_path, index_col = 0)
                        # print(f"shape: {combined_df.shape}")
                        result_df = pd.concat([result_df, combined_df])
                # go back to the dates directory
                os.chdir("..")
            except:
                pass
            os.chdir('..')
        result_shape = result_df.shape

    return result_df, result_shape
    # return_html = f"""
    # <p id="scraping" hx-swap="outerHTML">Resultant scraping shape for {search_term} | {today}: {result_shape}</p>
    # """
    # return return_html

# ---------------------------------------------------------------------------- #
#                           partial testing functions                          #
# ---------------------------------------------------------------------------- #

def test_cwd():
    # starting:
    # C:\Users\User\Desktop\programowanie_web_etc\python_projects\scrapers\job_scraping
    # os.chdir(r'./scraping_results/')
    cur_cwd = str(os.getcwd())
    return_html = f"""
    <p id="scraping_test" hx-swap="outerHTML">{cur_cwd}</p>
    """
    return return_html

def reset_path():
    root_path = app.root_path
    # instance_path = app.instance_path
    # file_path = os.path.abspath(__file__)
    os.chdir(root_path)
    os.chdir('..')
    cur_cwd = str(os.getcwd())
    return cur_cwd
    # return_html = f"""
    # <p id="scraping_test" hx-swap="outerHTML">{cur_cwd}</p>
    # """

    return return_html

def test_finding(search_term):
    path = ''
    today = str(date.today())
    test_path = path + r'./scraping_results/' + search_term + '/' + str(today)
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    # test_path += '/'
    os.chdir(test_path)
    return_html = test_cwd()
    return return_html