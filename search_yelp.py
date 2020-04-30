import pandas as pd
import numpy as np
import requests
import json
import os
# import yelp
from yelp.client import Client


yelp_client_id = os.environ['YELP_CLIENT_ID']
yelp_api_key = os.environ['YELP_API_KEY']

client = Client(yelp_api_key)

# define globally?
search_headers = {'Authorization': 'Bearer %s' % yelp_api_key}


def business_search_yelp():
    # TODO: add parameters as input arguments to this function

    url = 'https://api.yelp.com/v3/businesses/search'

    lat = 33.711247
    long = -115.984767
    # TODO: Get lat/long search params to work (why isn't it?)
    params = {
        'location': 'Riverside County, CA'
        # 'latitude:': lat
        # ,'longitude': long
        # ,'radius': 40000
        ,'limit': 50
        # ,'offset': 50
    }

    response = requests.get(url, params=params, headers=search_headers)
    # print(response.text)

    # proceed only if the status code is 200
    # TODO: Add try/except clause to deal with unexpected response behaviors
    print('The status code is {}'.format(response.status_code))

    # search_results_json = json.loads(response.text)

    search_results_df = pd.DataFrame.from_dict(response.json()['businesses'])

    return search_results_df


def business_details_yelp(yelp_id):
    business_id_url = "https://api.yelp.com/v3/businesses/{ID}".format(ID=yelp_id)
    business_details_response = requests.get(business_id_url, headers=search_headers)
    # print(business_details_response.text)

    details_df = pd.DataFrame.from_dict([business_details_response.json()])

    # details_dict = {'id': business_details_response.json()['id'],
    #                 'name': business_details_response.json()['name'],
    #                 'alias': business_details_response.json()['alias'],
    #                 'is_claimed': business_details_response.json()['is_claimed'], # greater confidence that profile has been updated
    #                 'review_count': business_details_response.json()['review_count'],
    #                 'categories': business_details_response.json()['categories'],
    #                 'is_closed': business_details_response.json()['is_closed'],
    #                 'zip_code': business_details_response.json()['location']['zip_code'],
    #                 'transactions:': business_details_response.json()['transactions']
    #                 }

    return details_df


# print(business_details_yelp('sQ-dABqseCrb07yjF3CbDA'))


def aggregate_details_from_search(search_results_df):
    details_list_to_agg = []
    yelp_id_list = search_results_df['id'].tolist()
    for yelp_id in yelp_id_list:
        details_list_to_agg.append(business_details_yelp(yelp_id))

    all_search_details_df = pd.concat(details_list_to_agg, sort=False)

    return all_search_details_df


search_riverside_ca = business_search_yelp()
details_riverside_ca = aggregate_details_from_search(search_riverside_ca)

print(details_riverside_ca.columns)
print(details_riverside_ca.head())
print(details_riverside_ca[['name', 'id', 'location', 'is_closed', 'is_claimed', 'transactions']])


def extract_zip_code(details_df_row):
    if len(details_df_row['location']['zip_code']) < 1:
        return None
    else:
        return details_df_row['location']['zip_code']


details_riverside_ca['zip_code'] = details_riverside_ca.apply(lambda row: extract_zip_code(row), axis=1)
print(details_riverside_ca[['id', 'name', 'zip_code']])

# TODO: Sample and collect a few cities/locations, aggregate into database

# TODO: Cross-reference businesses with FB, Google, etc? (by name, location?)
# TODO: Collect date/time of API call to track historical trends
# TODO: Store somewhere -- USDR database?
# TODO: Business closure rate, modified hours rate // by zipcode, category
# TODO: Identify Opportunity Zones (by zipcode)
