import pandas as pd
import requests
import os
import facebook


fb_token = os.environ['FB_ACCESS_TOKEN']
graph = facebook.GraphAPI(access_token=fb_token, version=3.1)

places = graph.search(type='place',
                      # center='33.666855,-115.871783',
                      # distance=100000,
                      fields='name,id,checkins,location,category_list,differently_open_offerings,hours,temporary_status',
                      q="riverside california"
                      )

for place in places['data']:
    try:
        print(place['name'], place['location'].get('zip'), place['hours'],
              place['temporary_status'], place['differently_open_offerings'], place['category_list'])
    except KeyError:
        print('ERROR ---- ', place['name'], place['location'].get('zip'), place['checkins'])


# grab place IDs using search
# for each place ID, grab open status (differently_open_offerings, hours, temporary_status)
