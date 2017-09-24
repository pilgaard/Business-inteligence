import pandas as pd
import numpy as np
import requests
import os
import csv
from osmread import parse_file, Node
from collections import defaultdict

def decode_node_to_csv():
    for entry in parse_file('./data/denmark-latest.osm'):
        if (isinstance(entry, Node) and
            'addr:street' in entry.tags and
            'addr:postcode' in entry.tags and
            'addr:housenumber' in entry.tags):

            yield entry

def save_geolocations(decoded_nodes):
    houses = pd.DataFrame([])
    lat = []
    lon = []

    for idx, decoded_node in enumerate(decoded_nodes):
        houses = houses.append(pd.DataFrame(decoded_node.tags, columns=['addr:street', 'addr:postcode', 'addr:housenumber'],index=[idx]))
        lat.append(decoded_node.lat)
        lon.append(decoded_node.lon)
    df = pd.DataFrame({'lat': lat, 'lon': lon}, columns=['lat', 'lon'])
    houses.columns = ['street', 'zipcode', 'addr:housenumber']
    houses["street"] = houses["street"].map(str) +" "+ houses["addr:housenumber"]

    df1 = pd.merge(houses, df, left_index=True, right_index=True)
    return df1

def merge_lists():
    housing_df = pd.read_csv('./boliga_all.csv')
    for value in housing_df:
        print(value)

def run():
    decoded_nodes = decode_node_to_csv()
    results = save_geolocations(decoded_nodes)
    results.to_csv("decoded_nodes.csv")

run()
