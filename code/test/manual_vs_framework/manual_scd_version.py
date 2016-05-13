import sqlite3
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def manual_scd_test(dbname, attr_value, version_value):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    start = time.monotonic()
    cur.execute("SELECT attr2 FROM scd "
                "WHERE attr2 = :attr_value AND version = "
                ":version_value", {'attr_value': attr_value,
                                   'version_value': version_value})

    rows = cur.fetchall()
    if rows.__len__() > 1:
        end = time.monotonic()
        elapsed = end - start
        print('FAILED More rows found: {}{}'.format(round(elapsed, 3), 's'))
        for row in rows:
            print(row)
    elif rows.__len__() < 1:
        end = time.monotonic()
        elapsed = end - start
        print('FAILED no rows: {}{}'.format(round(elapsed, 3), 's'))
    else:
        end = time.monotonic()
        elapsed = end - start
        print('SUCCESS: {}{}'.format(round(elapsed, 3), 's'))

