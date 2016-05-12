import sqlite3
import time

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


def TimePassed(start):
    end = time.monotonic()
    elapsed = end - start
    return '{}{}'.format(round(elapsed, 3), 's')


def manual_no_duplicates_test(path, table_name, column_names):
    start = time.monotonic()
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    if isinstance(column_names, str):
        column_names = [column_names]

    sql_command = 'SELECT {}'.format(column_names[0])
    column_names.pop(0)
    while column_names:
        sql_command += ',{}'.format(column_names[0])
        column_names.pop(0)
    sql_command += ' FROM {};'.format(table_name)
    cur.execute(sql_command)
    all_rows = cur.fetchall()
    rows_list = []
    rows_set = set()

    for row in all_rows:
        rows_list.append(row)
        rows_set.add(row)
        if len(rows_list) != len(rows_set):
            return print(False, TimePassed(start), 'Duplicate Row: {}'.format(row))

    return print(True, TimePassed(start))