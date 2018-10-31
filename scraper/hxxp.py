"""
Author: Miles Avelli
Last Updated: 10/31/2018
"""
import datetime
import argparse
import sqlite3
import re
import requests
# used pip install validators
import validators
from bs4 import BeautifulSoup

"""
Here is a list of accepted header ids, this can be expanded to
suit the users needs. If the user would want to expand the list,
the database would require reformatting, this can be done by request.
If a header id is not in this list, it is added to the misc column for
the database. If no header id value for a member of the list is given, 
it is left as an empty string.
"""

accepted_headers = ['date',
                    'cache-control',
                    'content-type',
                    'content-encoding',
                    'transfer-encoding',
                    'connection',
                    'misc']

def scrape(db,url):
    print("== Start Scraping ==")

    #open/create the database
    print("Open/creating " + str(db))
    try:
        conn = sqlite3.connect(db)
    except:
        raise Exception('Could not create database')
    print("Database open")
    c = conn.cursor()

    #issue HTTP request
    print("Issuing HTTP request to " + str(url))
    response = requests.get(url)
    response.raise_for_status()
    print("Received valid HTTP response")
    print("Stripping Headers")
    header_response = response.headers
    #make all the headers lowercase for easy access in dicitonaries
    header_response = {k.lower():v for k,v in header_response.items()}

    #get global list of accepted headers
    global accepted_headers

    #create new dictionary for storing extracted headers
    headers_data = dict.fromkeys(accepted_headers,"")

    #iterate over recieved headers, store in dictionary where applicable
    for h in header_response:
        if h in headers_data:
            headers_data[h] = header_response[h]
        else:
            headers_data['misc'] += str("{" + h + " : " + header_response[h] + "}, ")

    headers_data =list(headers_data.values())
    print("Parsing HTML document")
    #create a BeautifulSoup object for parsing the html response
    soup = BeautifulSoup(response.content, 'html.parser')

    #get head tag
    head = soup.find('head')

    #get body tag
    body = soup.find('body')

    # get today's date
    date = datetime.datetime.today().strftime('%Y%m%d')

    #convert to strings for database insertion
    head = str(head)
    body = str(body)

    #create data list for input
    html_data = [date, url, head, body]

    #try to create the database tables, if already created, pass
    try:
        c.execute("CREATE TABLE heads(date text, cachecontrol text, contenttype text, contentencoding text, transferencoding text, connection text, misc text)")
        c.execute("CREATE TABLE htmldata(date text, url text, head text, body text)")
    except:
        pass
    #push values into database
    print("Pushing headers to " + str(db))
    c.execute("INSERT INTO heads VALUES(?,?,?,?,?,?,?)",headers_data)
    print("Pushing HTML data to " + str(db))
    c.execute("INSERT INTO htmldata VALUES(?,?,?,?)", html_data)

    #commit changes and close connection
    print("Committing changes")
    conn.commit()
    print("Closing connection")
    conn.close()
    print("Push complete")
    print("== Scraping complete ==")
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='database path')
    parser.add_argument('url', help='url for scraping')
    args = parser.parse_args()

    #check for valid database name with regex
    d = re.compile('^.+?\.db$')
    if not re.fullmatch(d,args.db):
        raise ValueError('database given is not correct format, <name>.db')

    #check for valid url
    if not validators.url(args.url):
        raise ValueError('url given is not correct format, https://www.example.com or http://www.example.com')

    #scrape url and dump to database
    scrape(args.db, args.url)

    return

if __name__ == '__main__':
    main()
