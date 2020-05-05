import pandas as pd
import requests
import os
import facebook


fb_token = os.environ['FB_ACCESS_TOKEN']  # this access token will expire on June 29, 2020

try:
    graph = facebook.GraphAPI(access_token=fb_token, version=3.1)
except:
    print('Error: Unable to initialize Facebook Graph API access.')


def business_search_facebook():  # TODO: add params
    try:
        places = graph.search(type='place',
                              # center='33.666855,-115.871783',
                              # distance=100000,
                              fields='name,id,checkins,location,category_list,differently_open_offerings,hours,temporary_status',
                              q="palm springs, CA"
                              )
    except:
        print('Error: Facebook Graph API search invalid.')

    # TODO: Transform into DF?



# TODO: Functionize following steps, use output from business_search_facebook as input

# TODO: Issue: if a record has no data for a particular field, it will simply return the record with neither the
#  value NOR the key. Solution: create DF schema, then fill it with data/values or nulls as they come up.
for p in places['data']:
    try:
        info = graph.get_object(id=p['id'], fields="id,name,description,category_list,checkins,location,\
                                                   temporary_status,differently_open_offerings,hours,\
                                                   is_always_open,is_permanently_closed,\
                                                   is_verified,parking,payment_options,\
                                                   restaurant_services")
    except:
        info = None
        print('Error: invalid API call.')

    full_keys = ['id', 'name', 'description', 'category_list', 'checkins', 'location', 'temporary_status',
                 'differently_open_offerings', 'hours', 'is_always_open', 'is_permanently_closed', 'is_verified',
                 'parking', 'payment_options', 'restaurant_services']

    missing_fields = full_keys - p.keys()
    for m in missing_fields:
        info[m] = None

    print(info)
    # if 'temporary_status' in p.keys():
    #     print(p['id'], p['temporary_status'])


# TODO: Same as Yelp search -- for each ID retrieved by FB search, use Place Information endpoint to get more details

