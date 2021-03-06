__author__ = "Mathias Claus Jensen"

import os
import sqlite3
import names
import random

ENTRIES_BOOK = 100
ENTRIES_AUTHOR = 100
ENTRiES_COUNTRIES = 20

CITIES = ['Hadsten', 'Aalborg', 'Skanderborg', None, 'Kobenhavn']
COUNTRY_MAP = {city:country for city, country in zip(CITIES, ['DK' for x in CITIES])}
COUNTRY_MAP['Kobenhavn'] = 'SWE'

def get_conn_cur(path):
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)
    return conn, conn.cursor()

def mk_author_db(db_path="author.db", pops=500):
    """ Makes and Author DB and populates it
    :param db_path: the path where the DB is created
    :pops: The amount of entries that will be generated
    """

    conn, cur = get_conn_cur(db_path)

    cur.execute("""CREATE TABLE author (
                    aid INTEGER ,
                    firstname TEXT,
                    lastname TEXT,
                    city TEXT,
                    bid INTEGER)""")

    #Get This working....
    author_list = []
    author_list.extend ( [(0, 'Mathias', 'Jensen', 'Hadsten', 3),
                   (1, 'Mathias', 'Jensen', 'Hadsten', 4),
                   (2, 'Alexander', 'Danger', 'Skanderborg', 0),
                   (3, 'Alexander', 'Danger', 'Skanderborg', 4),
                   (6, 'Alexander', 'Danger', 'Hadsten', 4),
                   (4, 'Arash', 'Kjær', 'Kobenhavn', 1),
                   (5, 'Michael', 'Med K', None, 2)])


    for x in range(ENTRIES_AUTHOR):
        author_list.append((x+6, names.get_first_name(), names.get_last_name(),
                            random.choice(CITIES), x+6))

    cur.executemany("INSERT INTO author VALUES(?, ?, ?, ?, ?)", author_list)

    conn.commit()
    conn.close()

def mk_book_db(db_path="book.db"):
    conn, cur = get_conn_cur(db_path)

    cur.execute("CREATE TABLE book ("
                "bid INTEGER , "
                "title TEXT, "
                "year INTEGER)")

    book_list = []
    book_list.extend ([(0, "Checkm8 en Fortælling", 1994),
    (3, "EZ PZ ETL", 2000),
    (2, "Mit Navn Staves Med K", 2015),
    (1, "Svensk-Dansk Ordbog", 1995),
    (4, "EZ PZ ETL", 2004)])

    for x in range(ENTRIES_BOOK):
        book_list.append((x+4, names.get_first_name(), random.randrange(2000)))

    cur.executemany("INSERT INTO book VALUES(?, ?, ?)", book_list)

    conn.commit()
    conn.close()

def mk_country_csv(file_path="country.csv"):
    if os.path.exists(file_path):
        os.remove(file_path)


    with open(file_path, "+w") as f:
         f.write('city,country\n')
         f.write('Hadsten,DK \n')
         f.write('Skanderborg,DK \n')
         f.write('Kobenhavn,SWE \n')
