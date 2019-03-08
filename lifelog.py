"""
Log your life? No, just the little important things we tend to forget...
"""
import math
import sqlite3
import sys
import time
from collections import OrderedDict
from datetime import datetime
from itertools import islice
from time import mktime

from pathlib import Path

TIME_FORMAT = '%Y-%m-%d %H:%M'
DB_NAME = 'lldb'
DB_FILE = str(Path(__file__).resolve().parent / DB_NAME)
print(DB_FILE)


def save(entry):
    """Persist a log entry"""
    conn = db_conn()
    sql = "insert into log (datetime, entry) values(strftime('%s','now'), '{}')"
    conn.execute(sql.format(entry))
    conn.commit()


def escape_special_characters(entry):
    """Escape sqlite special characters"""
    # for now just '
    return entry.replace("'", "''")


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
    for _, seconds_since_epoch, entry in cur.fetchall():
        time_struct = time.gmtime(seconds_since_epoch)
        date_time = datetime.fromtimestamp(mktime(time_struct))
        lifelog[date_time] = entry
    return lifelog


def order_asc(lifelog):
    """Orders `lifelog` ASC making it far easier to query"""
    return OrderedDict(list(lifelog.items()))


def order_desc(lifelog):
    """Orders `lifelog` DESC making it far easier to query"""
    return OrderedDict(reversed(list(lifelog.items())))


def list_display(lifelog):
    """Preview display of all `lifelog` entries"""
    for datetime, entry in lifelog.items():
        print(datetime.strftime(TIME_FORMAT), end=': ')
        print(lifelog[datetime][:100], '...', sep='')


def detail_display(entry_datetime, entry_text):
    """Detail display of a single `lifelog` entry"""
    print(' ' * 45, end='')
    print(entry_datetime.strftime(TIME_FORMAT))
    print(' ' * 45)

    pos = 0
    while pos < len(entry_text):
        end = min(pos + 100, len(entry_text))
        print(entry_text[pos:end])
        pos = end


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_display(order_asc(lifelog(db_conn())))

    if len(sys.argv) == 1:
        save(
            escape_special_characters(
                str(input())
            )
        )

    if len(sys.argv) > 1 and '^' in sys.argv[1]:
        lifelog = order_desc(lifelog(db_conn()))
        entry_nbr = sys.argv[1].count('^') - 1
        datetime = (next(islice(lifelog.items(), entry_nbr, None)))[0]
        detail_display(datetime, lifelog[datetime])
