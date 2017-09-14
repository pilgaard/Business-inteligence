import bs4
import requests
import csv
import os
import re

def scrape_index(url):

    indexes = []

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')

    table = soup.find('table')
    table_body = table.find('tbody')

    links = table_body.find_all('a')
    del links [:5]

    links = [link.text for link in links]

    return links

def save_to_csv(data, path='./out/boliga.csv'):

    with open(path, 'w', encoding='utf-8') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['street', 'city', 'zipcode',
                                'no_rooms', 'size_in_sq_m',
                                'year_of_construction', 'price',
                                'sale_date_str'])

        for row in data:
            output_writer.writerow(row)

def scrape_housing_data(url):

    data = []

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')

    table = soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        # Decode address column
        links = cols[0].find_all('a')
        line = re.sub(r'<br/>', '\n',str(links[0]))
        _, line,_ = line.split('>')
        line,_ = line.split('<')
        street, town = line.split('\n')
        zip_code, city = town.split(' ',1)
        int(zip_code)

        # Decode number of rooms
        no_rooms_str = cols[4].text.strip()
        try:
            no_rooms = int(no_rooms_str)
        except:
            no_rooms = None
        # Decode selling date and type
        size_in_sq_m_str = cols[6].text.strip()
        try:
            size_in_sq_m = int(size_in_sq_m_str)
        except:
            size_in_sq_m = None
        # Decode year of construction
        year_of_construction_str = cols[7].text.strip()
        try:
            year_of_construction = int(year_of_construction_str)
        except:
            year_of_construction = None
        # Decode price
        price_str = cols[1].text.strip()
        try:
            price = float(price_str.replace('.',''))
        except:
            price = None
        # Decode sales date
        sale_date_str = cols[2].text.strip()
        sale_date = sale_date_str[:10]

        decoded_row = (street, city, zip_code, no_rooms,
                       size_in_sq_m, year_of_construction, price,
                       sale_date)
        data.append(decoded_row)

    print('Scraped {} sales...'.format(len(data)))

    return data

def save(base_url, urls):
    result = []
    for url in urls:
        u = os.path.join(base_url, url)
        result += scrape_housing_data(u)
    save_to_file = os.path.join(out_dir, os.path.basename(url).split('_')[0] + '.csv')
    save_to_csv(result, save_to_file)

def run():

    base_url = 'http://138.197.184.35/boliga/'
    urls = scrape_index(base_url)
    """    new_list = []
        area = ""

        for value in links:
            temp, _ = value.split('_')
            if not new_list or area == temp:
                new_list.append(value)

                #save(base_url, new_list)
            else:
                print(new_list)
                new_list = []
                area, _ = value.split('_')
    """
    new_list =[]
    count = 0

    for i in urls:
        _, number = i.split('_')
        number,_ = number.split('.')
        num= int(number)
        temp = count+1
        if num == temp:
            new_list.append(i)
            count+=1
        else:
            save(base_url, new_list)
            new_list = []
            count = 1
            new_list.append(i)

    save(base_url, new_list)

"""
    fst_fourty_results = scrape_housing_data(urls[0])
    snd_fourty_results = scrape_housing_data(urls[1])
    fst_results = fst_fourty_results + snd_fourty_results

    save_to_file = os.path.join(out_dir, os.path.basename(urls[0]).split('_')[1] + '.csv')
    save_to_csv(fst_results, save_to_file)

    last_results = scrape_housing_data(urls[2])
    save_to_file = os.path.join(out_dir, os.path.basename(urls[2]).split('_')[1] + '.csv')
    save_to_csv(last_results, save_to_file)
"""
out_dir = './data/out'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
run()
