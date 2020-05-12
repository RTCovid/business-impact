import os
import requests
import json

# API docs: https://developers.google.com/places/web-service/search

google_maps_api_key = os.environ['GOOGLE_MAPS_API_KEY']


def place_search_google():
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'

    params = dict(
        key=google_maps_api_key,
        input='mcdonalds',  # input required -- so, use 'name' fields retrieved from Yelp & FB searches?
        inputtype='textquery',
        fields='place_id,name,formatted_address,plus_code,business_status,permanently_closed,types',
        locationbias='rectangle:33.450393,-117.286647|34.071474,-114.496120'
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    return data


in_n_out_search = place_search_google()
for i in in_n_out_search['candidates']:
    print(i)

