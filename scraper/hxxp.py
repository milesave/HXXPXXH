import argparse
import requests
from bs4 import BeautifulSoup
from lxml import html

def scrape(url):
    #scrape here
    return




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='database path')
    parser.add_argument('url', help='url for scraping')
    args = parser.parse_args()
    print(args.url)
    print(args.db)

    scrape(args.url)

    return


if __name__ == '__main__':
    main()
