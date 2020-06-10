import pandas as pd
import requests
import os
from datetime import datetime
import facebook


def init_fb_graph_object(fb_access_token, api_version=3.1):
    try:
        graph = facebook.GraphAPI(access_token=fb_access_token, version=api_version)
    except:  # TODO: Better error handling (which exceptions to anticipate?)
        graph = None
        print('Error: Unable to initialize Facebook Graph API access.')

    return graph


def business_search_facebook(fb_graph, location_query=None, location_center=None, location_distance=None):
    """
    EITHER (location_center, location_distance) OR q are required as arguments.

    :param fb_graph: (obj) Facebook graph object initialized in init_fb_graph_object().
    :param location_query: (str) Query to search for location (ex: "san francisco, ca").
    :param location_center: (str) Coordinates in the form "latitude,longitude".
    :param location_distance: (int) Distance from coordinates provided, in meters (max value = ?).  # TODO: Assume there's a max value?
    :return: places: (list) FB Graph search results -- each record is a dict containing the fields ('name', 'id',
    'location' by default) as keys, and search results as values
    """
    if location_center and location_distance:
        try:
            search_results = fb_graph.search(type='place',
                                             center=location_center,
                                             distance=location_distance,
                                             fields='name,id,location'  # using these basic fields as default;
                                             # grab more details in business_details_facebook()
                                            )
        except:  # TODO: Better error handling (which exceptions to anticipate?) Also, logging?
            search_results = None
            print('Error: Facebook Graph API search invalid (coordinates and distance provided).')

    elif location_query:
        try:
            search_results = fb_graph.search(type='place',
                                             fields='name,id,location',
                                             q=location_query
                                             )
        except:  # TODO: Better error handling (which exceptions to anticipate?) Also, logging?
            search_results = None
            print('Error: Facebook Graph API search invalid (location query provided).')

    else:
        search_results = None
        print('Error: Neither (coordinates, distance) or location query were provided.')

    places = search_results['data']
    return places


def business_details_facebook(fb_graph, facebook_id, detail_fields):
    """
    :param fb_graph: (obj) Facebook graph object initialized in init_fb_graph_object().
    :param facebook_id: (str) Unique ID identifying a business found via FB Graph search.
    :param detail_fields: (str) Which of the available fields to include in results.
        Must be formatted exactly like: 'field1,field2,field3,...'
    :return: info: (dict) Dict containing details for the business associated with the business ID passed.
    """
    try:
        place_details = fb_graph.get_object(id=facebook_id, fields=detail_fields)
    except:  # TODO: Better error handling (which exceptions to anticipate?) Also, logging?
        place_details = None
        print("Error: Invalid 'get_object' API call.")

    full_keys = detail_fields.split(',')

    # If a record has no data for a particular field, the API call will simply return the record with neither
    # the value NOR the key. So, populate missing keys as None/null.
    missing_fields = full_keys - place_details.keys()
    for m in missing_fields:
        place_details[m] = None  # TODO: Or null/NA ?

    try:
        zip_code = place_details['location']['zip']
    except:
        zip_code = 'No zip code found'

    place_details['zip_code'] = zip_code

    return place_details


def all_business_details_facebook(fb_graph, places, detail_fields):
    details_list = []
    for p in places:
        details = business_details_facebook(fb_graph=fb_graph, facebook_id=p['id'], detail_fields=detail_fields)
        details_list.append(details)

    all_business_details_df = pd.DataFrame(details_list)
    all_business_details_df['api_call_datetime'] = datetime.now()

    return all_business_details_df


def main():
    fb_token = os.environ['FB_ACCESS_TOKEN']  # this access token will expire on June 29, 2020

    print('Initializing FB Graph object...')
    graph_obj = init_fb_graph_object(fb_token)

    print('Searching FB API...')
    palm_springs_places = business_search_facebook(graph_obj, location_query='palm springs, ca')

    detail_fields_1 = "id,name,description,category_list,checkins,location,temporary_status," \
                      "differently_open_offerings,hours," \
                      "is_always_open,is_permanently_closed," \
                      "is_verified,parking,payment_options," \
                      "restaurant_services"

    print('Getting details on each business...')
    palm_springs_details = all_business_details_facebook(graph_obj, palm_springs_places, detail_fields_1)
    print(palm_springs_details[['name', 'is_always_open']])

    return palm_springs_details


if __name__ == '__main__':
    palm_springs_details = main()
