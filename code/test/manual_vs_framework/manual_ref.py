import sqlite3
import time

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


def TimePassed(start):
    end = time.monotonic()
    elapsed = end - start
    return '{}{}'.format(round(elapsed, 3), 's')


def manual_ref(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    start = time.monotonic()

    cur.execute('PRAGMA foreign_key_list(ft1)')
    print(cur.fetchall())

    cur.execute('PRAGMA foreign_key_list(dim1)')
    print(cur.fetchall())

    cur.execute('PRAGMA foreign_key_list(dim2)')
    print(cur.fetchall())


    return print(True, TimePassed(start))
