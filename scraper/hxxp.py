import datetime
import argparse
import sqlite3
import re
import requests
# used pip install validators
import validators
from bs4 import BeautifulSoup

def scrape(db,url):
    #open/create the database
    try:
        conn = sqlite3.connect(db)
    except:
        raise Exception('could not create database')

    c = conn.cursor()

    #issue HTTP request
    response = requests.get(url)
    print(response.headers)
    print('\n')

    print(response.text)
    #create a BeautifulSoup object for parsing the html response
    soup = BeautifulSoup(response.content, 'html.parser')

    #get head
    head = soup.find('head')

    #get body
    body = soup.find('body')

    # get today's date
    date = datetime.datetime.today().strftime('%Y%m%d')

    #convert to strings for database insertion
    head = str(head)
    body = str(body)

    #create date list to input into database
    data_in = [date, head, body]

    #try to create the database, if already created, pass
    try:
        c.execute("CREATE TABLE scraped(date text, head text, body text)")
    except:
        pass

    #push values into database
    c.execute("INSERT INTO scraped VALUES(?,?,?)", data_in)

    #commit changes
    conn.commit()

    #close connection
    conn.close()

    return




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='database path')
    parser.add_argument('url', help='url for scraping')
    args = parser.parse_args()

    #check for valid database name
    d = re.compile('^.+?\.db$')
    if not re.fullmatch(d,args.db):
        raise ValueError('database given is not of the correct format, <name>.db')

    #check for valid url
    if not validators.url(args.url):
        raise ValueError('url given is not the correct format, https://www.example.com or http://www.example.com')

    #scrape url and dump to database
    scrape(args.db, args.url)

    return


if __name__ == '__main__':
    main()
