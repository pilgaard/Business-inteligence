
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import date
from datetime import datetime
import folium
import warnings
warnings.filterwarnings('ignore')
from mpl_toolkits.basemap import Basemap
import collections

def generate_basemap_for_copenhagen(dataframe):

    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
            width=5000000, height=5000000,
            lat_0=55, lon_0=10,)
    #m.etopo(scale=1.0, alpha=0.5)

    coords = generate_coord_sets(dataframe)
    xer=[]
    yer=[]
    for _, coord in coords.items():
        x, y = m(coord[1], coord[0])
        xer.append(x)
        yer.append(y)
    plt.plot(xer, yer, 'ok', markersize=5)

    fig.savefig('./data/copenhagen.png')

def get_dataframe_by_year(dataframe,requested_year):
    return dataframe[dataframe['sell_date'].dt.year == requested_year]

def get_dataframes_by_zip(dataframe,zip_list):
    return dataframe[dataframe['zip_nr'].isin(zip_list)]

def plot_haversine_from_copenhagen(dataframe):
    dataframe = dataframe.assign(km_to_cph=haversine_to_location(0,dataframe))
    return dataframe[dataframe['km_to_cph'] <= 50]

def haversine_to_location(mult,dataframe):
    if mult is 1:
        return dataframe.apply(lambda row: multiple_haversines(row),axis=1)
    else:
        return dataframe.apply(lambda row: calc_haversine(row),axis=1)

def calc_haversine(row,kfc=''):

    if kfc is not '':
        lat_orig, lon_orig = kfc
    else:
        lat_orig, lon_orig = (55.676111,12.568333)
    lat_dest = row['lat']
    lon_dest = row['lon']

    radius = 6371

    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(lon_dest-lon_orig)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat_orig))
        * math.cos(math.radians(lat_dest)) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def get_house_trade_freq_by_zipcode(dataframe):

    unique_zips = dataframe['zip_nr'].unique()
    unique_zips.sort()

    sales_by_zip = collections.OrderedDict()

    for zip in unique_zips:
        no_of_sales = len(dataframe[dataframe['zip_nr'] == zip])
        sales_by_zip[zip] = no_of_sales

    return sales_by_zip

def generate_coord_sets(df):
    lats = df['lat']
    longs = df['lon']
    coords = {}

    for idx, row in df.iterrows():
        coords[row['address']] = (row['lat'], row['lon'])
    return coords

def generate_plot(x,y):
    fig = plt.figure()

    y[::-1].sort()
    x.sort()

    plt.plot(x,y,'ro')
    plt.xlabel('pris Per m2, i tusinde')
    plt.ylabel('Distance')
    plt.gca().invert_yaxis()

    fig.savefig('./data/nørreport_sales.png')

def generate_folium_map(dataframe):
    my_map = folium.Map(location=[55.88207495748612, 10.636574309440173], zoom_start=6)

    for coords in zip(dataframe.lon.values, dataframe.lat.values):
        if not np.isnan(coords[0]):
            folium.CircleMarker(location=[coords[1], coords[0]], radius=2).add_to(my_map)

    my_map.save('./data/folium.html')

def generate_distance_plot(dataframe):

    dataframe = dataframe.assign(km_to_nrp=haversine_to_location(0,dataframe))

    y = dataframe['km_to_nrp'].values
    x = dataframe['price_per_sq_m'].values

    generate_plot(x,y)

def generate_histogram_for_sales_by_zip(sales_by_zip):

    fig = plt.figure(figsize=(80,20))

    x = []
    y = []
    for zip, no_of_sales in sales_by_zip.items():
        x.append(zip)
        y.append(no_of_sales)

    plt.bar(x,y,align='center')

    fig.savefig('./data/sales_by_zip.png')
