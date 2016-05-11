import os
import sqlite3
import pygrametl
from pygrametl.tables import Dimension, FactTable
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def setup(dbname, number):

    open(os.path.expanduser(dbname), 'w')

    output_conn = sqlite3.connect(dbname)
    output_cur = output_conn.cursor()

    output_cur.execute("CREATE TABLE dim1 "
                       "(key1 INTEGER PRIMARY KEY, attr1 INTEGER, "
                       "attr2 INTEGER)")

    output_cur.execute("CREATE TABLE dim2 "
                       "(key2 INTEGER PRIMARY KEY, attr3 INTEGER, "
                       "attr4 INTEGER)")

    output_cur.execute("CREATE TABLE ft1 "
                       "(measure INTEGER, key1 INTEGER, key2 INTEGER, "
                       "PRIMARY KEY(key1, key2))")

    output_conn.commit()
    output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

    dim1 = Dimension(
        name='dim1',
        key='key1',
        attributes=['attr1', 'attr2']
    )

    dim2 = Dimension(
        name='dim2',
        key='key2',
        attributes=['attr3', 'attr4'],
    )

    ft1 = FactTable(
        name='ft1',
        keyrefs=['key1', 'key2'],
        measures=['measure']
    )

    facts = []
    dim1_data = []
    dim2_data = []

    total_elapsed = 0.
    print('Generating ft1 data')
    start = time.monotonic()
    counter = 0
    for i in range(1, number + 1):
        for j in range(1, number + 1):
            counter += 10
            facts.append({'key1': i, 'key2': j, 'measure': counter})
    end = time.monotonic()
    elapsed = end - start
    print('Generated: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('Generating dim1 data')
    start = time.monotonic()
    for i in range(1, number + 1):
        dim1_data.append({'attr1': i, 'attr2': number + 1 - i})
    end = time.monotonic()
    elapsed = end - start
    print('Generated: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('Generating dim2 data')
    start = time.monotonic()
    for i in range(1, number + 1):
        dim2_data.append({'attr3': i, 'attr4': number + 1 - i})
    end = time.monotonic()
    elapsed = end - start
    print('Generated: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('Inserting data into ft1')
    start = time.monotonic()
    for row in facts:
        ft1.insert(row)
    end = time.monotonic()
    elapsed = end - start
    print('Inserted: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('Inserting data into dim1')
    start = time.monotonic()
    for row in dim1_data:
        dim1.insert(row)
    end = time.monotonic()
    elapsed = end - start
    print('Inserted: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('Inserting data into dim2')
    start = time.monotonic()
    for row in dim2_data:
        dim2.insert(row)
    end = time.monotonic()
    elapsed = end - start
    print('Inserted: {}{}'.format(round(elapsed, 3), 's'))
    total_elapsed += elapsed

    print('DW populated')
    print('Total time: {}{}\n'.format(round(total_elapsed, 3), 's'))

    output_conn.commit()
