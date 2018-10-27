# HXXPXXH

## Overview

HXXPXXH is a tool that scrapes web pages.  It is split in to two tools, HXXP
and PXXH.

Upon execution, HXXP will connect to the URL, issue an HTTP request, and
receive an HTTP response.  The HTTP response will be separated in to its HTTP
headers and body and stored in a SQLITE database in appropriate tables.

Some time later, a user will query the database and retrieve the records
that were entered for a day using PXXH.  If no records exist, then the tool
will print nothing.  If records exist, then the tool will print the
reconstructed HTTP requests for the day (e.g. the headers and body for each
request made on a day).

## Usage

HXXP is executed as follows:

```
python hxxp.py --db <DB_PATH> <URL>
```

Concretely,

```
python hxxp.py --db sqlite.db https://www.example.com
```

PXXH is executed as follows:

```
python pxxh.py --db <DB_PATH> <TIMESTAMP: YYYYMMDD>
```

Concretely,

```
python pxxh.py --db sqlite.db 20180530
```

## Definitions

DB_PATH is a sqlite database (default: sqlite.db).
URL is an HTTP or HTTPS url to connect to (e.g. https://www.example.com).
TIMESTAMP is a 4-digit Year, 2-digit Month, 2-digit Day formatted timestamp.

## Requirements

The tool should:

0. Work.

1. Include any instructions for installing or using it.

(e.g. build an egg and install it).

