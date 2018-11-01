from datetime import datetime
import sqlite3
import re
import argparse

def query(db, timestamp):
    try:
        conn = sqlite3.connect(db)
    except:
        raise Exception('Could not create database')
    print('Database open')
    c = conn.cursor()

    c.execute("SELECT * FROM heads WHERE heads.datekey = ?", (timestamp,))
    headers = c.fetchall()
    header_col_names = [description[0] for description in c.description]

    c.execute("SELECT * FROM htmldata WHERE htmldata.Date = ?", (timestamp,))
    html = c.fetchall()
    c.close()

    # check to see if something was found
    if len(headers) is 0 or len(html) is 0:
        print('No entries found for ' + str(timestamp))
        print('Exiting...')
        return

    rtnd = len(html)

    print(str.center('', 80, '='))

    print(str.center('All entries acquired on ' + timestamp,80, '='))

    for i in range(0, rtnd):
        # header dictionary, will hold headers for output
        header_dict = dict(zip(header_col_names, headers[i]))

        misc = header_dict['misc'].split('}, ')

        #format and insert misc contents into header dictionary
        for j in range(0, len(misc)):
            if len(misc[j]) == 0:
                misc.pop(j)
            else:
                misc[j] = re.sub('[{]', '',misc[j])
                t = misc[j].split(' : ')
                header_dict[t[0]] = t[1]

        #remove the misc header from header dictionary
        header_dict.pop('misc')
        header_dict.pop('datekey')

        #format html data
        date, url, head, body = html[i]

        #print stuff
        print(str.center('',80,'='))
        print('URL: ' + url + '\n')
        print('Header from HTTP response\n')
        for k,v in header_dict.items():
            print(k + ' : ' + v)
        print('\nHTML head\n')
        print(head)
        print('\nHTML body\n')
        print(body + '\n')
        print(str.center('',80,'='))

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='database path')
    parser.add_argument('timestamp', help='timestamp for database pull')
    args = parser.parse_args()

    #check for valid database name
    d = re.compile('^.+?\.db$')
    if not re.fullmatch(d,args.db):
        raise ValueError('database given is not correct format, <name>.db')

    try:
        datetime.strptime(args.timestamp,'%Y%m%d')
    except ValueError:
        print('timestamp given is not correct format, only valid YYYYMMDD')

    #query the database
    query(args.db, args.timestamp)

    return

if __name__ == '__main__':
    main()