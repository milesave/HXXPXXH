## Instructions

## Python Version 
3.6 or newer

## Modules
Install these modules, required for hxxp.py and pxxh.py to function as expected.

pip install beautifulsoup4

pip install validators

## How to use HXXPXXH (also in README.md)

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
