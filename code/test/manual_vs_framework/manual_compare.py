import sqlite3
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def manual_compare_test(path, number):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    expected_rows = []
    counter = 0
    print('Generating expected table')
    start = time.monotonic()
    for i in range(1, number + 1):
        for j in range(1, number + 1):
            counter += 10
            expected_rows.append((counter, i, j))

    end = time.monotonic()
    elapsed = end - start
    print('Done: {}{}'.format(round(elapsed, 3), 's'))

    start = time.monotonic()
    cur.execute("SELECT * FROM ft1")
    error_rows = []
    #  This might not actually work, infinite loop
    while expected_rows.__len__() > 0:
        row = cur.fetchone()
        if row not in expected_rows:
            error_rows.append(row)
        else:
            expected_rows.remove(row)

    if error_rows:
        result = False
    else:
        result = True

    if result:
        print('Manual OK')
    elif not result:
        print('Manual FAILED')
        for row in error_rows:
            print(row)

    end = time.monotonic()
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))
