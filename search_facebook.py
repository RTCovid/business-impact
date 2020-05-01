import pandas as pd
import requests
import os
import facebook


fb_token = os.environ['FB_ACCESS_TOKEN']  # this access token will expire on June 29, 2020
graph = facebook.GraphAPI(access_token=fb_token, version=3.1)

places = graph.search(type='place',
                      # center='33.666855,-115.871783',
                      # distance=100000,
                      fields='name,id,checkins,location,category_list,differently_open_offerings,hours,temporary_status',
                      q="palm springs, CA"
                      )

# TODO: Create DF schema, then fill it with data, because some records don't have every field
for p in places['data']:
    # print(p)
    if 'temporary_status' in p.keys():
        print(p['id'], p['temporary_status'])
    # try:
    #     print(p['name'], p['location'].get('zip'), p['hours'],
    #           p['temporary_status'], p['differently_open_offerings'], p['category_list'])
    # except KeyError:
    #     print('ERROR ---- ', p['name'], p['location'].get('zip'), p['checkins'])

# TODO: if KeyError (value does not exist), fill with null

# TODO: Same as Yelp search -- for each ID retrieved by FB search, use Place Information endpoint to get more details

# for each place ID, grab open status (differently_open_offerings, hours, temporary_status)
