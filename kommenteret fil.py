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
# her åbner vi en fil til skrive kun i binært format. Vi overskriver filen, hvis filen findes.
# Hvis filen ikke findes, opretter vi en ny fil til skrivning.
# og vi refere til denne fil som f
    with open(save_path, 'wb') as f:
# her skriver vi så det indhold som findes i response ind i vores fil f.
        f.write(response.content)

# her definerer vi en metode kaldet generate_csv som tagere to parametre txt_input_path og csv_output_path
def generate_csv(txt_input_path, csv_output_path):
# her åbner vi en fil som vi får fra vores parameter txt_input_path og siger den skal skrives i utf-8 format og vi vil referer til filen som f
    with open(txt_input_path, encoding='utf-8') as f:
# vi laver et objekt txt_content som indeholder teksten fra vores fil f
        txt_content = f.readlines()
# her laver vi et todimensionelt array og som indeholderen 5 værdier i den første række
    rows = [['street', 'city', 'price', 'sqm', 'price_per_sqm']]
# her laver vi en for-lykke som køre igennem hver linie i txt_content
    for line in txt_content:
# her sætter vi line til at være lig med line, men hvor vi har fjernet '  * ' og erstatet det med ''
        line = line.rstrip().replace('  * ', '')
# her splitter vi line på tab og sætter den forskellige substrings til address, price og sqm
        address, price, sqm = line.split('\t')
# her splitter vi så address hvor vi har  '; ' og sætter substringsne til street og city
        street, city = address.split('; ')
# vi laver en ny variabel price_per_sqm som er lig med price divideret med sqm. vi bruger to forwardslash for at få værdien som heltal
        price_per_sqm = int(price) // int(sqm)
# vi laver en række som består af street, city, price, sqm og price_per_sqm
        row = (street, city, price, sqm, price_per_sqm)
# herefter indsætter vi rækken i vores array
        rows.append(row)

# her har vi et if statement som tjekker om operativsystemet som koden bliver kørt på er Windows
    if platform.system() == 'Windows':
# hvis den er det bliver newline sat til en tom string
        newline=''
    else:
# hvis det ikke er Windows, bliver newline sat til None, som er det samme som mange andre sprogs NULL værdi
        newline=None

# her åbner vi en fil i skrivetilstand, vi referer til filen som csv_output_path.
# Vi fortæller med newline=newline hvordan vi ønsker at terminate en linie da dette skal gøres forskelligt afhængig af om vi bruger windows eller ej
# vi ønsker at skrive i utf-8 format, og så vil vi gerne referer til filen som f
    with open(csv_output_path, 'w', newline=newline, encoding='utf-8') as f:
# her laver vi et writer object kaldet output_writer som skal bruges til at skrive til f i csv format
        output_writer = csv.writer(f)
# vi køre igennem en for-lykke
        for row in rows:
# og siger for hver row i rows skal vi skrive vores row til output_writer
            output_writer.writerow(row)

# Vi definerer en metode kaldet read_prices, metoden tager et parameter kaldet csv_input_path
def read_prices(csv_input_path):
# vi åbner en fil csv_input_path med utf-8 encoding, og vi vil referertil filen som f
    with open(csv_input_path, encoding='utf-8') as f:
#vi laver et reader objekt som kan læse vores csv fil f
        reader = csv.reader(f)
# vi bruger next(reader) til at springe over den første linie i vores csv fil.
# vi bruger _ som en "smid væk variabel"
        _ = next(reader)

# vi laver et array kaldet idxs
        idxs = []
# vi laver et array kaldet prices
        prices = []
# vi laver en for-lykke på vores reader
        for row in reader:
# vi bruger underscore som en "smid væk variabel", så vi er kun interesseret i price variablen fra vores row
            _, _, price, _, _ = row
# vi gemmer linie nummeret fra reader i vores indxs array
            idxs.append(reader.line_num)
# vi gemmer price variablen som en int i vores prices array
            prices.append(int(price))
#til sidst returnere vi en liste af datasæt bestående af idxs og prices
    return list(zip(idxs, prices))

# vi definerer en metode kaldet compute_avg_price som tager et parameter data
def compute_avg_price(data):
# vi unzipper vores data, og siger vi kun er interesseret i prices
    _, prices = zip(*data)
# vi beregner gennemsnitspriserne fra data og gemmer det i en variabel avg_price
    avg_price = statistics.mean(prices)
# vi åbner en fil /tmp/avg_price.txt i skrivetilstand i utf-8 encoding og vil refere til den som f
    with open('/tmp/avg_price.txt', 'w', encoding='utf-8') as f:
# her skriver vi så avg_price ind i filen som en string
        f.write(str(avg_price))
# til sidst returnere vi avg_price
    return avg_price

# vi definerer en metode generate_plot som tager data som parameter
def generate_plot(data):
# vi unzipper data og gennem dens to værdier som x_values og y_values
    x_values, y_values = zip(*data)
# vi opretter en figur
    fig = plt.figure()
# vi indsætter x og y værdierne som et koordinat i vores figur med en prik der har en størelse på 100
    plt.scatter(x_values, y_values, s=100)
# til sidst gemmer vi figuren som prices.png i det directory vi befinder os i.
# vi bruger bbox_inches='tight' til at fjerne alt den overskydende plads rund om vores figur 
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
