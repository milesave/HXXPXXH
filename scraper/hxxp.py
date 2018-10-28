import argparse
import sqlite3
import re
import requests
# used pip install validators
import validators
from bs4 import BeautifulSoup
from lxml import html

def scrape(db,url):

    #open/create the database
    try:
        conn = sqlite3.connect(db)
    except:
        raise Exception('could not connect to database')
    c = conn.cursor()

    #issue HTTP request
    response = requests.get(url)
    headers = response.headers
    doc = html.fromstring(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('body')
    h = soup.find('head')
    print(body)
    print('\n')
    print(headers)
    print('\n')
    print(h)



    #scrape here
    return




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='database path')
    parser.add_argument('url', help='url for scraping')
    args = parser.parse_args()

    print(args.url)
    print(args.db)

    #check to see if given valid database name
    d = re.compile('^.+?\.db$')
    if not re.fullmatch(d,args.db):
        raise ValueError('database given is not of the correct format, <name>.db')

    #check for valid url
    if not validators.url(args.url):
        raise ValueError('url given is not the correct format, https://www.example.com or http://www.example.com')

    #scrape url and dump to database
    scrape(args.db,args.url)

    return


if __name__ == '__main__':
    main()
