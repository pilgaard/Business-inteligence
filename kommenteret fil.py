# her har vi en del moduler som bliver importeret ind i programmet
import os
import csv
import requests
import platform
import statistics
import matplotlib
# her får matplotlib at vide det skal bruge agg
matplotlib.use('agg')
# her importere vi igen et modul og derefter omdøber det til plt
import matplotlib.pyplot as plt

# her definerer vi en metode kaldet download_txt, metoden tager to argumenter url og save_path.
# save_path har en sti som er den mappe man befinder sig i nu og hopper derfra ind i mappen "downloaded"
def download_txt(url, save_path='./downloaded'):
# vi laver et response object som er den hjemmeside vi får fra requests.get(url)
    response = requests.get(url)
#
    with open(save_path, 'wb') as f:
        f.write(response.content)


def generate_csv(txt_input_path, csv_output_path):
    with open(txt_input_path, encoding='utf-8') as f:
        txt_content = f.readlines()

    rows = [['street', 'city', 'price', 'sqm', 'price_per_sqm']]
    for line in txt_content:
        line = line.rstrip().replace('  * ', '')
        address, price, sqm = line.split('\t')
        street, city = address.split('; ')
        price_per_sqm = int(price) // int(sqm)
        row = (street, city, price, sqm, price_per_sqm)
        rows.append(row)

    if platform.system() == 'Windows':
        newline=''
    else:
        newline=None

    with open(csv_output_path, 'w', newline=newline, encoding='utf-8') as f:
        output_writer = csv.writer(f)
        for row in rows:
            output_writer.writerow(row)


def read_prices(csv_input_path):
    with open(csv_input_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        _ = next(reader)

        idxs = []
        prices = []
        for row in reader:
            _, _, price, _, _ = row
            idxs.append(reader.line_num)
            prices.append(int(price))

    return list(zip(idxs, prices))


def compute_avg_price(data):
    _, prices = zip(*data)
    avg_price = statistics.mean(prices)

    with open('/tmp/avg_price.txt', 'w', encoding='utf-8') as f:
        f.write(str(avg_price))

    return avg_price


def generate_plot(data):

    x_values, y_values = zip(*data)
    fig = plt.figure()
    plt.scatter(x_values, y_values, s=100)
    fig.savefig('./prices.png', bbox_inches='tight')


def run():
    file_url = 'https://raw.githubusercontent.com/datsoftlyngby/' \
               'soft2017fall-business-intelligence-teaching-material/master/' \
               'assignments/assignment_1/price_list.txt'
    txt_file_name = os.path.basename(file_url)
    txt_path = os.path.join('./', txt_file_name)
    download_txt(file_url, txt_path)
    csv_file_name = 'price_list.csv'
    csv_path = os.path.join(os.getcwd(), csv_file_name)
    generate_csv(txt_path, csv_path)
    data = read_prices(csv_path)
    avg_price = compute_avg_price(data)
    print(avg_price)
    generate_plot(data)

# her har vi en condition der tjekker om vores __name__ variable er lig med '__main__'
if __name__ == '__main__':
# og til sidst køre vi hele programmet
    run()
