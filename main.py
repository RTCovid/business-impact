import pandas as pd
import requests
# import facebook2  # TODO
import yelp
import os
import json
import search_google
import search_facebook


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

google_places = search_google.place_search_google(creds['google-maps-api-key'], 'mcdonalds')
google_places_df = search_google.parse_results_google(google_places)


fb_graph_obj = search_facebook.init_fb_graph_object(creds['facebook-graph-api-token'])
fb_places = search_facebook.business_search_facebook(fb_graph_obj, "riverside county, ca")
print(fb_places)
