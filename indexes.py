import bs4
import requests
import csv
import os

url = "http://138.197.184.35/boliga/"
def scrape_index(url):

    indexes = []

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'html5lib')

    table = soup.find('table')
    table_body = table.find('tbody')

    links = table_body.find_all('a')
    del links [:5]

#    for link in links:
#        print(link.get("href"))

    return links
