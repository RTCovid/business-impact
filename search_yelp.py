import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime
# import yelp
from yelp.client import Client


# yelp_client_id = os.environ['YELP_CLIENT_ID']
# yelp_api_key = os.environ['YELP_API_KEY']
#
# client = Client(yelp_api_key)

# define globally?



def business_search_yelp(creds, search_params):
    search_url = 'https://api.yelp.com/v3/businesses/search'

    search_headers = {'Authorization': 'Bearer %s' % creds['yelp_api_key']}

    response = requests.get(search_url, params=search_params, headers=search_headers)
    # print(response.request.url)
    # print(response.text)

    # proceed only if the status code is 200
    if response.status_code == 200:
        # search_results_json = json.loads(response.text)
        search_results_df = pd.DataFrame.from_dict(response.json()['businesses'])  # TODO: Keep this as json/dict for now (don't make into DF)
        return search_results_df

    else:
        print('Non-200 status code: {}'.format(response.status_code))
        print(response.text)
        return None  # TODO: ???


def loop_offset_search(creds, search_params):
    search_dfs_list = [business_search_yelp(creds, search_params)]
    # print(search_dfs_list)
    offset_mult = 1
    while offset_mult < 20 and search_dfs_list[-1].shape[0] == 50:
        # Conditioning on `offset_mult < 20` to avoid Yelp API error: `{"error": {"code": "VALIDATION_ERROR", "description": "Too many results requested, limit+offset must be <= 1000."}}`
        # TODO: If approaching 1000 results, change offset to get only exactly 1000, no more (<= 1000)
        print('---------------------- Looping through results... ----------------------')
        print('More data available...most recent scraped data # rows:', search_dfs_list[-1].shape[0])
        print('Num DFs in list:', len(search_dfs_list))
        search_params['offset'] = 50 * offset_mult
        print('Num results:', search_params['offset'], '+/- 49')
        search_dfs_list.append(business_search_yelp(creds, search_params))
        offset_mult += 1

    all_search_results_df = pd.concat(search_dfs_list)
    # TODO: Dedupe DF just in case there truly are exactly 50 results?

    return all_search_results_df


def business_details_yelp(creds, yelp_id):
    business_id_url = "https://api.yelp.com/v3/businesses/{ID}".format(ID=yelp_id)

    search_headers = {'Authorization': 'Bearer %s' % creds['yelp_api_key']}
    business_details_response = requests.get(business_id_url, headers=search_headers)
    # print(business_details_response.text)

    details_df = pd.DataFrame.from_dict([business_details_response.json()])

    # TODO: Explain how these fields can indicate great confidence that profile has been updated recently?
    # details_dict = {'id': business_details_response.json()['id'],
    #                 'name': business_details_response.json()['name'],
    #                 'alias': business_details_response.json()['alias'],
    #                 'is_claimed': business_details_response.json()['is_claimed'],
    #                 'review_count': business_details_response.json()['review_count'],
    #                 'categories': business_details_response.json()['categories'],
    #                 'is_closed': business_details_response.json()['is_closed'],
    #                 'zip_code': business_details_response.json()['location']['zip_code'],
    #                 'transactions:': business_details_response.json()['transactions']
    #                 }

    return details_df


def aggregate_details_from_search(creds, search_results_df):
    details_list_to_agg = []
    yelp_id_list = search_results_df['id'].tolist()
    for yelp_id in yelp_id_list:
        details_list_to_agg.append(business_details_yelp(creds, yelp_id))

    all_search_details_df = pd.concat(details_list_to_agg, sort=False)
    # TODO: Re-index?

    return all_search_details_df


def extract_zip_code(details_df_row):
    # print('--------------------------------------------------------')
    # print(details_df_row['location'])
    # print(type(details_df_row['location']))
    # print(details_df_row['location']['zip_code'])
    # print(type(details_df_row['location']['zip_code']))
    try:
        if details_df_row['location']:
            if not isinstance(details_df_row['location']['zip_code'], str):
                return str(details_df_row['location']['zip_code'])
            elif len(details_df_row['location']['zip_code']) < 1:
                return None
            else:
                return details_df_row['location']['zip_code']
        else:
            print('NO ZIP CODE: ', details_df_row['id'], details_df_row['location'])
            return 'No zip code found'
    except Exception as e:
        print(f"Error extracting ZIP code from location ({e})")
        return f'No zip code found (exception {e}).'


def run_full_search(creds, search_params):
    print("Searching for results matching '{}'...".format(search_params['location']))
    search_df = loop_offset_search(creds, search_params)
    print('\nGetting details on all matching businesses (may take a few minutes)...')
    details_df = aggregate_details_from_search(creds, search_df)
    details_df['api_call_location_query'] = search_params['location']
    # print(details_df.columns)
    # print(details_df.head())
    # print(details_df[['name', 'id', 'location', 'is_closed', 'is_claimed', 'transactions']])
    details_df['zip_code'] = details_df.apply(lambda row: extract_zip_code(row), axis=1)
    details_df['api_call_datetime'] = datetime.now()
    # details_df['api_call_location_query'] = search_params['location']
    # print(details_df[['id', 'name', 'zip_code']])

    return details_df




