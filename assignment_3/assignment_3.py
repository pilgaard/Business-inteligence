import pandas as pd
import numpy as np
import requests
import os

###########################################
######## ADDING COLUMN TO 2D ARRAY ########
"""test_twodim = np.array([[ 1,  2, 3, 4],
                        [ 1,  2, 3, 4],
                        [ 1,  2, 3, 4]])
test_df = pd.DataFrame(test_twodim)
array_to_add = np.array([[1],
                       [1],
                       [1]])
test_df['new_col'] = array_to_add"""
##########################################

path = "../assignment_2/data/boliga_all.csv"
housing_df = pd.read_csv(path)

def get_address_from_dataframe():
    addresses = housing_df["street"].values ## Dette virker ikke
    return addresses

def get_location_for(address):
    api_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    try:
        r = requests.get(api_url, params={'sensor': 'false',
                                          'address': address})
        results = r.json()['results']

        location = results[0]['geometry']['location']
        lat, lon = location['lat'], location['lng']
    except:
        lat, lon = None, None
    return lat, lon

print(get_location_for("Tranevej 68A"))


def get_all_locations(addresses):
    for address in addresses:
        return get_location_for(address)
