import pandas as pd
import numpy as np
import requests
import os
import platform
import csv
from osmread import parse_file, Node
from collections import defaultdict

boliga = "./data/boliga_all.csv"

def decode_node_to_csv():
    for entry in parse_file('./data/denmark-latest.osm'):
        if (isinstance(entry, Node) and
            'addr:street' in entry.tags and
            'addr:postcode' in entry.tags and
            'addr:housenumber' in entry.tags):

            yield entry

def save_geolocations():
    #vi læser vores boliga fil ind og laver den til et data frame
    tdataframe = pd.read_csv(boliga)
    # vi laver to nye dataframes "lat" og "lon" og siger værdierne er "not a number"
    tdataframe['lat'] = np.nan
    tdataframe['lon'] = np.nan

    setup_dataframe_csv()

    dataframe = concat(tdataframe)

    dataframe.set_index("api_addresses", inplace=True)

    for idx, decoded_node in enumerate(decode_node_to_csv()):
        try:
            geocoded_address = (decoded_node.tags['addr:street'] + " " + decoded_node.tags['addr:housenumber'] + " " + decoded_node.tags['addr:postcode'] + " " + decoded_node.tags['addr:city'], decoded_node.lon, decoded_node.lat)

            if dataframe.loc[geocoded_address[0]] is not None:
                dataframe.set_value(geocoded_address[0], 'lon', geocoded_address[1])
                dataframe.set_value(geocoded_address[0], 'lat', geocoded_address[2])
        except (KeyError, ValueError):
            pass

    dataframe.to_csv("./data/geo_data.csv", sep=',', encoding='utf-8')

def concat(dataframe):
    api_addresses = [' '.join([a.split(',')[0], str(z)]) for a, z in dataframe[['street', 'zipcode']].values]
    dataframe = dataframe.assign(api_addresses=api_addresses)
    dataframe = dataframe.drop_duplicates(subset="api_addresses")

    return dataframe

def newline():
    # vi tjekker vores OS for hvide hvordan vi skal lave en ny linje
    if platform.system() == 'Windows':
        return ''
    else:
        return None

def setup_dataframe_csv():
    if not os.path.exists("data/geo_data.csv"):
        # Output the .csv file in the working directory.
        title_row = ("address","zip_code","price","sell_date","sell_type","price_per_sq_m","no_rooms","housing_type","size_in_sq_m","year_of_construction","price_change_in_pct","longitude","latitude")
        with open("data/geo_data.csv", 'w', newline=newline(), encoding='utf-8') as f:
            output_writer = csv.writer(f)
            output_writer.writerow(title_row)

def run():
    decoded_nodes = decode_node_to_csv()
    save_geolocations(decoded_nodes)

run()
