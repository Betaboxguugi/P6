""" This file contains a number of function for creating the necessary resources required for example_1.py
"""
__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'

# IMPORTS
import sqlite3
import os


def setup_input_db(sales_db_name='./sales.db'):
    """ This function sets up the DB that will be used as an input for the ETL
    """
    # If the some DB with our name already exists, delete it!
    if os.path.exists(sales_db_name):
        os.remove(sales_db_name)

    # We connect to our DB and make a cursor    
    sales_conn = sqlite3.connect(sales_db_name)
    sales_cur = sales_conn.cursor()

    # We make a new table
    sales_cur.execute("CREATE TABLE sales " +
                        "(saleid INTEGER PRIMARY KEY, book TEXT, genre TEXT, city TEXT, " +
                        "timestamp TEXT, sale INT)")

    # The stuff we wanna put in our table
    sales_list = [('Nineteen Eighty-Four', 'Novel', 'Aalborg', '2005/08/05', 50),
                  ('Calvin and Hobbes One', 'Comic', 'Aalborg', '2005/08/05',  25),
                  ('The Silver Spoon', 'Cockbook', 'Aalborg', '2005/08/14',  5),
                  ('The Silver Spoon', 'Cockbook', 'Odense', '2005/09/01',  7)]

    # We do a series of INSERT operation with before mentioned list
    sales_cur.executemany("INSERT INTO sales(book, genre, city, timestamp, sale) " + 
                           "VALUES(?, ?, ?, ?, ?)", sales_list)

    # We save all this to our DB and close it
    sales_conn.commit()
    sales_conn.close()

    
def setup_out_dw(dw_name='./dw.db'):
    """ This function sets up the DW in which the ETL will out put to
    """
    # Delete the DB if it already exists
    if os.path.exists(dw_name):
        os.remove(dw_name)
    
    dw_conn = sqlite3.connect(sales_dw_name)
    dw_cur = dw_conn.cursor()

    # We make a table for each dimension and the FactTable
    dw_cur.execute("CREATE TABLE bookDim " +
                        "(bookid INTEGER PRIMARY KEY, book TEXT, genre TEXT)")

    dw_cur.execute("CREATE TABLE locationDim " +
                        "(locationid INTEGER PRIMARY KEY, city TEXT, region TEXT)")

    dw_cur.execute("CREATE TABLE timeDim " +
                        "(timeid INTEGER PRIMARY KEY, day INT, month INT, year INT)")

    dw_cur.execute("CREATE TABLE factTable " +
                        "(bookid INTEGER, locationid INTEGER, " +
                        "timeid INTEGER, sale INT, PRIMARY KEY(bookid, locationid, timeid))")

    dw_conn.commit()   
    dw_conn.close()
    

def setup_input_csv(csv_name='./region.csv'):
    """ This function sets up the input CSV required
    """
    with open(csv_name, 'w+') as file:
        file.write('city,region\n')
        file.write('Aalborg,North Denmark Region\n')
        file.write('Odense,Region of Southern Denmark\n')

      



