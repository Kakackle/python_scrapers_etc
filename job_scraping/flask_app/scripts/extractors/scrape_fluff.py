"""
-> Get data from nofluffjobs hidden API through a request
-> transform it to conform to the Listing data model
-> Save to a csv file
-> Return a dataframe with collected

requires:
search_term - technology/term to search for
folder_path - base path to which to save the files
"""

import requests
import os
import pandas as pd
import json
from datetime import datetime, date
from globals import NUMBER_OF_PAGES

def scrape_fluff(search_term, folder_path):

    today = date.today()

    # url = "https://nofluffjobs.com/api/search/posting?page=1&limit=50&salaryCurrency=PLN&salaryPeriod=month&region=pl"

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

    api_results=[]
    for page in range(1, NUMBER_OF_PAGES):
        page_url = f"https://nofluffjobs.com/api/search/posting?page={page}&limit=50&salaryCurrency=PLN&salaryPeriod=month&region=pl"
        page_r = requests.request("POST", page_url, headers=headers, data=payload)
        page_data = page_r.json()
        page_postings = page_data['postings']
        for post in page_postings:
            api_results.append(post)
    #     print('page postings: ',len(page_postings))
    # print('postings half: ', len(api_results))

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
    listing_df.insert(listing_df.columns.get_loc('company')+1, 'location', '')
    listing_df.insert(listing_df.columns.get_loc('salary')+1, 'description', '')
    listing_df.insert(listing_df.columns.get_loc('skills')+1, 'search_term', search_tech.lower())
    listing_df.insert(listing_df.columns.get_loc('search_term')+1, 'date_searched', date.today())
    listing_df['date_added'] = listing_df['date_added'].apply(lambda x: datetime.fromtimestamp(x/1000).date())

    # save results
    save_path = folder_path + r'/nofluff'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path += '/'
    listing_df.to_csv(save_path + f'nofluff_{search_term}_{today}.csv')
    
    api_df = listing_df
    return api_df