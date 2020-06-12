import pandas as pd
import requests
import os
import json
from datetime import datetime

# import facebook2  # TODO
import yelp

import search_google
import search_facebook
import search_yelp

import google_bq_helper_functions

import pandas_gbq
from google.cloud import bigquery


def load_creds():
    """
    creds.json schema:
    {
    }

    Since `creds.json` is in .gitignore, create the file in your local copy of the project when you clone it.

    :return: creds (dict): Contains relevant credentials for logging into various API services.
    """

    cred_path = "creds.json"
    if not os.path.isfile(cred_path):
        print('ERROR: No file called `creds.json` found in the path.')
        return None

    creds = json.load(open(cred_path,))
    return creds


creds = load_creds()


# ====================================== GOOGLE API SEARCH & APPEND ====================================== #

def google_search_append(query):
    google_places = search_google.place_search_google(creds['google-maps-api-key'], query)
    # print(google_places)
    google_places_df = search_google.parse_results_google(google_places)
    google_places_df['api_call_location_query'] = query
    # print(google_places_df.head())

    gbq_creds = google_bq_helper_functions.load_gbq_creds()
    gbq_project_id = gbq_creds['project_id']
    gbq_google_table_id = 'business_data.google_data' # TODO: Put this in creds.json

    google_bq_helper_functions.append_df_gbq(google_places_df, gbq_google_table_id, gbq_project_id)

    print(f"Appended {google_places_df.shape[0]} row(s) to {gbq_google_table_id}.")

    return google_places_df


# google_places_df = google_search_append('El Campanario Restaurant')


# ====================================== FACEBOOK API SEARCH & APPEND ====================================== #

# fb_token = search_facebook.get_long_lived_user_access_token(creds)
# print(fb_token)
# TODO: Write/save this to creds.json along with get_timestamp;
#  if current time >= get_timestamp + 'expires_in' seconds + buffer, get new token, else use that token

def fb_search(location_query):
    fb_graph_obj = search_facebook.init_fb_graph_object(creds['fb-longlived-access-token'])

    # location_query = 'palm springs, ca'  # TODO: Make this an argument for the entire function?

    print(f"Searching FB API for '{location_query}'...")
    fb_api_places = search_facebook.business_search_facebook(fb_graph_obj, location_query=location_query)

    detail_fields_1 = "id,name,description,category_list,checkins,location,temporary_status," \
                      "differently_open_offerings,hours," \
                      "is_always_open,is_permanently_closed," \
                      "is_verified,parking,payment_options," \
                      "restaurant_services"

    print('Getting details on each business...')
    fb_api_details_df = search_facebook.all_business_details_facebook(fb_graph_obj, fb_api_places, detail_fields_1)
    fb_api_details_df['api_call_location_query'] = location_query

    return fb_api_details_df


# cities_location_query = ['indio, ca', 'palm springs, ca', 'palm desert, ca', 'riverside, ca', 'moreno valley, ca', 'temecula, ca']

def fb_search_append_gbq(location_query):
    fb_api_df = fb_search(location_query)

    gbq_creds = google_bq_helper_functions.load_gbq_creds()
    gbq_project_id = gbq_creds['project_id']
    gbq_fb_table_id = 'business_data.facebook_data'

    google_bq_helper_functions.append_df_gbq(fb_api_df, gbq_fb_table_id, gbq_project_id)


# fb_search_append_gbq('moreno valley, ca')


# ====================================== YELP API SEARCH & APPEND ====================================== #

# TODO: Get lat/long search params to work (why isn't it??)
#  Getting error: "{"error": {"code": "VALIDATION_ERROR", "description": "Please specify a location or a latitude and longitude"}}"
lat = float(33.769327)
long = float(-116.312849)
rad = int(4000)
params_lat_long = {
    'latitude:': lat,
    'longitude': long,
    'radius': rad
}


def yelp_search_append(query):
    search_params = {
        'location': query,
        'limit': 50  # max number of results to return at one time = 50
    }
    # TODO: Searching by 'location' parameter can return erroneous results
    #  (businesses in other similar-sounding cities, etc) -- validate results by zipcode obtained from location in details?

    yelp_api_df = search_yelp.run_full_search(creds, search_params)
    # yelp_api_df.to_pickle("./palm_springs.pkl")
    # yelp_api_df = pd.read_pickle("./palm_springs.pkl")
    # print(yelp_api_df.shape)
    # print(yelp_api_df.columns)
    print(yelp_api_df.head())
    print(yelp_api_df.columns)

    print(yelp_api_df.groupby(by=['is_closed', 'is_claimed'], as_index=False)['id'].agg('count'))

    gbq_creds = google_bq_helper_functions.load_gbq_creds()
    gbq_project_id = gbq_creds['project_id']
    gbq_yelp_table_id = 'business_data.yelp_data'

    google_bq_helper_functions.append_df_gbq(yelp_api_df, gbq_yelp_table_id, gbq_project_id)


yelp_search_append('indio, ca')

# gbq_creds = google_bq_helper_functions.load_gbq_creds()
# sql = "select * from `business_data.yelp_data`"
# df = google_bq_helper_functions.read_gbq_df(sql, gbq_creds['project_id'])
# print(df.head())


# TODO: Cross-reference businesses with FB, Google, etc? (by name, location?) Yelp business match: https://www.yelp.com/developers/documentation/v3/business_match
# TODO: Business closure rate, modified hours rate // segment by zip_code, biz category
# TODO: Identify Opportunity Zones (by zip_code)

# TODO: Hypothesis: economic activity in OZs is statistically significantly lower than that in non-OZs? Or is this too much further than 'just the facts'?
