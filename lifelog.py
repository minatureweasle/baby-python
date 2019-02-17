"""
Log your life? No, just the little important things we tend to forget...
"""
import math
import sqlite3
import sys
import time


def save(entry):
    """Persist a log entry"""
    conn = db_conn()
    sql = "insert into log (datetime, entry) values(strftime('%s','now'), '{}')"
    conn.execute(sql.format(entry))
    conn.commit()


def db_conn():
    """Connect to a database and setup table if required"""
    conn = sqlite3.connect('lldb')
    conn.cursor().execute((
        'create table if not exists log'
        '(id integer primary key autoincrement, '
        'datetime integer, '
        'entry text)'
    ))
    return conn


def lifelog(conn):
    """Extract our lifelog from the db into memory"""
    lifelog = {}
    cur = conn.execute('select * from log')
    for _, datetime, entry in cur.fetchall():
        lifelog[time.gmtime(datetime)] = entry
    return lifelog


def read(entry_datetime, entry_text):
    """Read an entry 100 characters at a time"""
    print(' ' * 45, end='')
    print(
        entry_datetime.tm_year,
        entry_datetime.tm_mon,
        entry_datetime.tm_mday,
        sep='-',
        end=''
    )
    print(' ' * 45)
    pos = 0
    while pos < len(entry_text):
        end = min(pos+100, len(entry_text))
        print(entry[pos:end])
        pos = end


if __name__ == '__main__':
    if len(sys.argv) > 1 and '^' in sys.argv[1]:
        lifelog = lifelog(db_conn())
        datetimes_sorted = sorted(lifelog.keys(), reverse=True)
        nbr_entries_back = sys.argv[1].count('^') - 1
        if len(datetimes_sorted) <= nbr_entries_back:
            sys.exit(0)
        datetime = datetimes_sorted[nbr_entries_back]
        entry = lifelog[datetimes_sorted[nbr_entries_back]]
        read(datetime, entry)

    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        lifelog = lifelog(db_conn())
        for datetime in sorted(lifelog.keys(), reverse=True):
            print(datetime.tm_year, datetime.tm_mon, datetime.tm_mday, sep='-', end=': ')
            print(lifelog[datetime][:100], '...', sep='')

    if len(sys.argv) == 1:
        save(str(input()))
