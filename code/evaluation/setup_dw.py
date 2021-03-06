import sqlite3
import os

__author__ = "Mathias Claus Jensen"


def mk_dw(dw_path='./dw.db'):
    if os.path.exists(dw_path):
        os.remove(dw_path)

    conn = sqlite3.connect(dw_path)
    cur = conn.cursor()

    # facttable
    cur.execute("CREATE TABLE facttable ("
                "aid INTEGER, "
                "bid INTEGER)")

    # BookDim
    cur.execute("CREATE TABLE bookdim ("
                "bid INTEGER, "
                "title TEXT, "
                "year INTEGER, "
                "version INTEGER)")

    # BookDim
    cur.execute("CREATE TABLE goodbooksdim ("
                "bid INTEGER, "
                "title TEXT, "
                "year INTEGER, "
                "version INTEGER)")

    company_info = [(1, 'The Hobbit', 1937, 4),
                    (2, 'Divine Comedy', 1320, 1)
                ]

    # ... and inserting the necessary data.
    cur.executemany("INSERT INTO goodbooksdim (BID,TITLE,YEAR,VERSION) VALUES (?,?,?,?)",
                  company_info)

    # AuthorDim
    cur.execute("CREATE TABLE authordim ("
                "aid INTEGER, "
                "name TEXT, "
                "city TEXT, "
                "cid INTEGER)")

    # CountryDim
    cur.execute("CREATE TABLE countrydim ("
                "cid INTEGER, "
                "country TEXT)")

    conn.commit()
    conn.close()
