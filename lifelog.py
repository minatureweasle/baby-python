"""
Log your life? No, just the little important things we tend to forget...
"""
import math
import sqlite3
import sys
import time
from collections import OrderedDict
from itertools import islice

DB_FILE = 'lldb'

def save(entry):
    """Persist a log entry"""
    conn = db_conn()
    sql = "insert into log (datetime, entry) values(strftime('%s','now'), '{}')"
    conn.execute(sql.format(entry))
    conn.commit()


def db_conn():
    """Connect to the database"""
    conn = sqlite3.connect(DB_FILE)
    # setup if required
    conn.cursor().execute((
        'create table if not exists log'
        '(id integer primary key autoincrement, '
        'datetime integer, '
        'entry text)'
    ))
    return conn


def lifelog(conn):
    """Load `lifelog` from the db into memory"""
    lifelog = {}
    cur = conn.execute('select * from log')
    for _, datetime, entry in cur.fetchall():
        lifelog[time.gmtime(datetime)] = entry
    return lifelog


def order(lifelog):
    """Orders `lifelog` making it far easier to query"""
    return OrderedDict(reversed(list(lifelog.items())))


def list_display(lifelog):
    """Preview display of all `lifelog` entries"""
    for datetime, entry in lifelog.items():
        print(datetime.tm_year, datetime.tm_mon, datetime.tm_mday, datetime.tm_hour, datetime.tm_min, sep='-', end=': ')
        print(lifelog[datetime][:100], '...', sep='')


def detail_display(entry_datetime, entry_text):
    """Detail display of a single `lifelog` entry"""
    print(' ' * 45, end='')
    print(
        entry_datetime.tm_year,
        entry_datetime.tm_mon,
        entry_datetime.tm_mday,
        entry_datetime.tm_hour,
        entry_datetime.tm_min,
        sep='-',
        end=''
    )
    print(' ' * 45)
    pos = 0
    while pos < len(entry_text):
        end = min(pos+100, len(entry_text))
        print(entry_text[pos:end])
        pos = end


if __name__ == '__main__':
    if len(sys.argv) > 1 and '^' in sys.argv[1]:
        lifelog = order(lifelog(db_conn()))
        entry_nbr = sys.argv[1].count('^') - 1
        datetime = (next(islice(lifelog.items(), entry_nbr, None)))[0]
        detail_display(datetime, lifelog[datetime])

    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_display(order(lifelog(db_conn())))

    if len(sys.argv) == 1:
        save(str(input()))
