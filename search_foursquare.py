import pandas as pd
import json
import requests
import os
from datetime import datetime
import foursquare

foursquare_client_id = os.environ['FOURSQUARE_CLIENT_ID']
foursquare_client_secret = os.environ['FOURSQUARE_CLIENT_SECRET']

def venue_search_foursquare():
    url = 'https://api.foursquare.com/v2/venues/search'

    params = dict(
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        # near='riverside, CA',
        intent='browse',
        sw='33.450393,-117.286647',
        ne='34.071474,-114.496120',
        v='20200511'
        # ll='40.7243,-74.0018',
        # query='coffee'
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    return data


def print_search_data(search_data):
    # if data['meta']['code'] == 200:
        # print(data['response'])

    for v in search_data['response']['venues']:
        print(v['name'], v['id'], v['location'])
        try:
            print(v['location']['postalCode'])
        except:
            pass


# TODO: Authorize user to access API (https://developer.foursquare.com/docs/places-api/authentication/)
#  (currently getting error 403)
def foursquare_venue_stats(venue_id):
    venue_stats_url = 'https://api.foursquare.com/v2/venues/timeseries'

    params = dict(
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        venueId=venue_id,
        startAt=1284286794,
        fields='totalCheckins,newCheckins,uniqueVisitors,sharing,genders,ages,hours',
        v='20200511'
    )

    resp = requests.get(url=venue_stats_url, params=params)
    data = json.loads(resp.text)

    return data


lost_palm_oasis_data = foursquare_venue_stats('58ed90cf92ca4c1a6fe480e9')
print(lost_palm_oasis_data)
