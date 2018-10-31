import datetime
import sqlite3
import re
import argparse
import validators

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
        print('timestamp given is not correct format, YYYYMMDD')



    return

if __name__ == '__main__':
    main()