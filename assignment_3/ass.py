import pandas as pd
import numpy as np
import requests
import os
import csv
from osmread import parse_file, Node
from collections import defaultdict


pathboliga = "./data/boliga_all.csv"
pathosm = "./data/denmark-latest.osm"

def add_geocode():
    df = pd.read_csv(pathboliga)

    tdataframe = df

    tdataframe['lat'] = np.nan
    tdataframe['lon'] = np.nan

    dataframe = concat(tdataframe)

    dataframe.set_index("api_addresses", inplace=True)

    for idx, decoded_node in enumerate(decode_node_to_csv(pathosm)):
        try:
            geocoded_address = (decoded_node.tags['addr:street'] + " " + decoded_node.tags['addr:housenumber'] + " " + \
                           decoded_node.tags['addr:postcode'] + " " + decoded_node.tags['addr:city'], decoded_node.lon, decoded_node.lat)

            #print(geocoded_address[0])
            if dataframe.loc[geocoded_address[0]] is not None:
                dataframe.set_value(geocoded_address[0], 'lon', geocoded_address[1])
                dataframe.set_value(geocoded_address[0], 'lat', geocoded_address[2])

            #print(dataframe)
        except (KeyError, ValueError):
            pass

    dataframe.to_csv("./data/geo_data.csv", sep=',', encoding='utf-8')


def decode_node_to_csv(file):
    for entry in parse_file(file):

        if (isinstance(entry, Node) and
                    'addr:street' in entry.tags and
                    'addr:postcode' in entry.tags and
                    'addr:housenumber' in entry.tags and
                    'addr:city' in entry.tags):
            yield entry

def concat(dataframe):
    api_addresses = [' '.join([a.split(',')[0], str(z)]) for a, z in dataframe[['street', 'zipcode']].values]
    dataframe = dataframe.assign(api_addresses=api_addresses)
    dataframe = dataframe.drop_duplicates(subset="api_addresses")

    return dataframe


add_geocode()
