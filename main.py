import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool, TimeoutError
import os

def main():
    start = datetime.now()

    url = 'https://coinmarketcap.com/all/views/all/';

    all_links = get_all_links(get_html(url))

    with Pool(25) as p:
        p.map(all_do, all_links)

    end = datetime.now()
    print("start: ", start )
    print("end: ", end )

    print("time: ", end - start)

def all_do(url):
    html = get_html(url['link'])
    data = get_data_from_page(html)
    file_writer(url['position'],data)

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id="currencies-all").find('tbody').find_all('tr')

    links = []

    for tr in trs:
        links.append({
            "link": 'https://coinmarketcap.com'+tr.find('a', class_="currency-name-container").get('href'),
            "position" : tr.find('td', class_="text-center").text.strip()
        })

    return links

def get_data_from_page(html):
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


def file_writer(position,data):
    with open('data/prices1.csv', "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow((position, data["name"], data["price"]))

        print(data["name"], "parsed")

if __name__ == '__main__':
    main()
