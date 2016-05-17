__author__ = "Mathias Claus Jensen"

import os
import sqlite3


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

    cur.execute("CREATE TABLE author (" \
                "aid INTEGER PRIMARY KEY, " \
                "firstname TEXT, " \
                "lastname TEXT, " \
                "city TEXT, " \
                "bid INTEGER)")

    author_list = [(0, 'Mathias', 'Jensen', 'Hadsten', 3),
                   (1, 'Mathias', 'Jensen', 'Hadsten', 4),
                   (2, 'Alexander', 'Danger', 'Skanderborg', 0),
                   (3, 'Alexander', 'Danger', 'Skanderborg', 4),
                   (4, 'Arash', 'Kjær', 'København', 1),
                   (5, 'Michael', 'Med K', None, 2)]

    cur.executemany("INSERT INTO author VALUES(?, ?, ?, ?, ?)", author_list)

    conn.commit()
    conn.close()

def mk_book_db(db_path="book.db"):
    conn, cur = get_conn_cur(db_path)

    cur.execute("CREATE TABLE book (" \
                "bid INTEGER PRIMARY KEY, " \
                "title TEXT, " \
                "year INTEGER)")
   
    book_list = [(0, "Checkm8 en Fortælling", 1994),
                 (3, "EZ PZ ETL", 2000),
                 (2, "Mit Navn Staves Med K", 2015),
                 (1, "Svensk-Dansk Ordbog", 1995),
                 (4, "EZ PZ ETL", 2004)]

    cur.executemany("INSERT INTO book VALUES(?, ?, ?)", book_list)
    

    conn.commit()
    conn.close()

def mk_country_csv(file_path="country.csv"):
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "+w") as f:
        s = \
"""city,country
Hadsten,DK
Skanderborg,DK
København,SWE
"""
        f.write(s)
