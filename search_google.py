import requests
import json
import pandas as pd

# API docs: https://developers.google.com/places/web-service/search


def place_search_google(google_maps_api_key, google_input):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'

    params = dict(
        key=google_maps_api_key,
        input=google_input,  # input required -- so, use 'name' fields retrieved from Yelp & FB searches?
        inputtype='textquery',
        fields='place_id,name,formatted_address,plus_code,business_status,permanently_closed,types',
        locationbias='rectangle:33.450393,-117.286647|34.071474,-114.496120'
    )

    # TODO: Add try/except & if/else for response == 200
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    return data


def parse_results_google(results):
    df = pd.DataFrame.from_records(results['candidates'])
    return df
