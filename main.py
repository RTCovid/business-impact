import pandas as pd
import requests
import os
import json
from datetime import datetime

# import facebook2  # TODO
import yelp

import search_google
import search_facebook

import google_bq_helper_functions

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

# google_places = search_google.place_search_google(creds['google-maps-api-key'], 'starbucks')
# print(google_places)
# google_places_df = search_google.parse_results_google(google_places)
# print(google_places_df)


# fb_token = search_facebook.get_long_lived_user_access_token(creds)
# print(fb_token)
# TODO: Write/save this to creds.json along with get_timestamp;
#  if current time >= get_timestamp + 'expires_in' seconds + buffer, get new token, else use that token

def fb_search():
    fb_graph_obj = search_facebook.init_fb_graph_object(creds['fb-longlived-access-token'])
    fb_places = search_facebook.business_search_facebook(fb_graph_obj, "riverside county, ca")
    print(fb_places)


def bq_connect():
    bq_creds = google_bq_helper_functions.load_bq_creds()

    print(bq_creds['project_id'])
    print(bq_creds['client_id'])

    file_id = None
    dataset_id = creds['google-bq-dataset-id']
    table_id = creds['google-bq-tables']['table1_test']
    google_bq_helper_functions.load_csv_bq(file_id, dataset_id, table_id)


# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_gbq.html

bq_connect()



# Connect to BQ
# Create tables (once)
# Update tables (add records, or download tables & add records & re-upload tables)