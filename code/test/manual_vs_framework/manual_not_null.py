import sqlite3
import time

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


def TimePassed(start):
    end = time.monotonic()
    elapsed = end - start
    return '{}{}'.format(round(elapsed, 3), 's')


def manual_not_null_test(path, table_name, column_names):
    start = time.monotonic()
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if isinstance(column_names, str):
        column_names = [column_names]
    for column in column_names:
        cur.execute('SELECT {} FROM {}'.format(column, table_name))
        for e in cur.fetchall():
            if e[0] is None:
                return print(False, TimePassed(start))
    return print(True, TimePassed(start))
