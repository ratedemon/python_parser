import os
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool, TimeoutError

class Parser:
    def __init__(self, url):
        self.url = url
        self.all_links = self.get_all_links(self.get_html(str(self.url)+'/all/views/all/'));
        i = 1
        while (os.path.exists('data/prices'+str(i)+'.csv')):
            i+=1
        self.path = 'data/prices'+str(i)+'.csv'

    def start(self):
        start = datetime.now()

        url = 'https://coinmarketcap.com';

        with Pool(25) as p:
            p.map(self.all_do, self.all_links)

        end = datetime.now()

        print("time: ", end - start)

    def all_do(self, url):
        html = self.get_html(url['link'])
        data = self.get_data_from_page(html)
        self.file_writer(url['position'],data)

    def get_html(self,link):
        # for n in links:
            # print(n)
        r = requests.get(link)
        return r.text

    def get_all_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        trs = soup.find('table', id="currencies-all").find('tbody').find_all('tr')

        links = []

        for tr in trs:
            links.append({
                "link": self.url+tr.find('a', class_="currency-name-container").get('href'),
                "position" : tr.find('td', class_="text-center").text.strip()
            })

        return links

    def get_data_from_page(self, html):
        soup = BeautifulSoup(html, 'lxml')

        try:
            name = soup.find('h1').text.strip()
        except Exception as e:
            name = ''

        try:
            price = soup.find('span', class_="text-large2").text.strip()
        except Exception as e:
            price = ''

        data = {"name": name, "price": price}

        return data

    def file_writer(self, position, data):
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow((position, data["name"], data["price"]))

            print(data["name"], "parsed")
