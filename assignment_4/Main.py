import Assignment_4 as asg
import pandas as pd

def run():
    df = setup()
    opg4(df)

def opg1(df):
    sales_2015 = asg.get_dataframe_by_year(df,2015)
    cities_in_50km = asg.plot_haversine_from_copenhagen(sales_2015)
    asg.generate_basemap_for_copenhagen(cities_in_50km)

def opg2(df):
    zip_list = []
    zip_list.extend(range(1050,1549))
    zip_list.extend([5000,8000,9000])

    fol = asg.get_dataframes_by_zip(df,zip_list)
    asg.generate_folium_map(fol)

def opg3(df):
    zip_list = []
    zip_list.extend(range(1000,3670))
    zip_list.extend(range(4000,4793))
    sales_2005 = asg.get_dataframe_by_year(df,2005)

    noerreport = asg.get_dataframes_by_zip(sales_2005,zip_list)
    noerreport = noerreport[noerreport['price_per_sq_m'] >= 80.000]
    asg.generate_distance_plot(noerreport)

def opg4(df):
    sales_by_zip = asg.get_house_trade_freq_by_zipcode(df)
    asg.generate_histogram_for_sales_by_zip(sales_by_zip)


def setup():
    complete_data = './data/boliga_all_loc.csv'

    df = pd.read_csv(complete_data)

    df = pd.read_csv(complete_data, parse_dates=['sell_date'])

    pd.to_datetime(df['sell_date'])

    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%Y')

    df = pd.read_csv(complete_data, parse_dates=['sell_date'], date_parser=dateparse)

    df['zip_nr'] = [int(el.split(' ')[0])
            for el in df['zip_code'].values]

    df['sell_year'] = df['sell_date'].dt.year
    return df

run()
