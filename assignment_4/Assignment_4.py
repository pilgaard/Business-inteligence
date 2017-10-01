
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from mpl_toolkits.basemap import Basemap

def hej():
    complete_data = './data/boliga_all_loc.csv'

    df = pd.read_csv(complete_data)

    df = pd.read_csv(complete_data, parse_dates=['sell_date'])
    print(df.head())

    pd.to_datetime(df['sell_date'])

    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%Y')

    df = pd.read_csv(complete_data, parse_dates=['sell_date'], date_parser=dateparse)
    print(df.head())

    df['zip_nr'] = [int(el.split(' ')[0])
                for el in df['zip_code'].values]

    df['sell_year'] = df['sell_date'].dt.year

    mask = ((df['zip_nr'] < 4800) &
            (df['sell_year'] <= 2005) &
            (df['sell_year'] >= 2000))
    df_zealand_00_05 = df[mask]
    print(df_zealand_00_05.head())


    plt.figure(figsize=(5, 5))
    m = Basemap(projection='ortho', resolution=None, lat_0=50, lon_0=10)
    m.bluemarble(scale=0.5)

    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection='lcc', resolution=None,
                width=5000000, height=5000000,
                lat_0=55, lon_0=10,)
    m.etopo(scale=1.0, alpha=0.5)

    # Map (long, lat) to (x, y) for plotting
    coords = {'København': (55.676111, 12.568333),
              'Odense': (55.395833, 10.388611),
              'Aalborg': (57.05, 9.916667)}

    for city, coord in coords.items():
        y_adjust = 100000 if city is 'Odense' else 0

        x, y = m(coord[1], coord[0])
        plt.plot(x, y, 'ok', markersize=5)

        plt.text(x + 50000, y - y_adjust, city, fontsize=8)

    mask = ((~df_zealand_00_05.lat.isnull()) &
            (~df_zealand_00_05.lon.isnull()) &
            (df_zealand_00_05.no_rooms >= 5))
    df_zealand_00_05_large = df_zealand_00_05[mask]

    for key, value in coords.items():
        x_values=value[0]
        y_values=value[1]
    # create new figure, axes instances.
    fig = plt.figure()
    ax = fig.add_axes([x_values.min(), y_values.min(),
                       x_values.max(), y_values.max()])

    # setup mercator map projection.
    m = Basemap(llcrnrlon=7., llcrnrlat=54.,
                urcrnrlon=16., urcrnrlat=58.,
                rsphere=(6378137.00, 6356752.3142),
                resolution='h', projection='merc',
                lat_0=40., lon_0=-20., lat_ts=20.)

    m.drawcoastlines()
    m.fillcontinents(zorder=0)
    m.scatter(df_zealand_00_05_large.lon.values,
              df_zealand_00_05_large.lat.values,
              3, marker='o', latlon=True)

    # draw parallels
    m.drawparallels(np.arange(10, 90,  1),
                    labels=[1, 1, 0, 1])
    # draw meridians
    m.drawmeridians(np.arange(-180, 180, 1),
                    labels=[1, 1, 0, 1])
    ax.set_title('Big Flats on Zealand')
    fig.savefig('./data/copenhagen_haver.png')
    plt.show()

#def setup():

def run():
#    setup()
    hej()

run()
