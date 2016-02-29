"""My own little test place, figuring out pygrametl"""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sys
import os.path
import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
from pygrametl.steps import *
import sqlite3
from step_funcs import *

# Insuring fresh database to work with by deleting old one
if os.path.isfile('test.db'):
   os.remove('test.db')
   print("Deleted previous database")
   conn = sqlite3.connect('test.db')
else:
   conn = sqlite3.connect('test.db')

c = conn.cursor()

# CONSTANTS

# Going to try and make this.
# http://www.dataonfocus.com/wp-content/uploads/2015/04/snowflake-schema-example.png

def setup_in_db(db_name='./db.db'):

    if os.path.exists(db_name):
        os.remove(db_name)

    db_conn = sqlite3.connect(db_name)
    db_cur = db_conn.cursor()

    db_cur.executescript("""CREATE TABLE sales(
                            sale_ID INT,
                            price INT,
                            currency TEXT,
                            location TEXT,
                            address TEXT,
                            worker_name TEXT,
                            age INT,
                            contact TEXT,
                            position_name TEXT,
                            salary INT,
                            PRIMARY KEY (sale_ID)
                            """)
    sale_list = [(100, 'usd', 'here', 'fakestreet', 'jim', 35, '+1 456 798 435', 'lawyer', 10),
                 (200, 'dkk', 'der', 'iranvej', 'lars', 41, '+45 23 23 23 23', 'ehvervsmand', 50),
                 (230, 'eur', 'there', 'roma', 'pepe', 22, '+39 56 87 34 54', 'rare', 5),
                 (9000, 'yen', 'far', 'battlecruiser', 'yamato', 112, '+81 345 354 894', 'admiral', 5000000)]

    db_cur.executemany("INSERT INTO sales(price, currency, location, address, name, age, contact, position_name, " +
                       "description, salary) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sale_list)

    db_conn.commit()
    db_conn.close()
    print("Operation done successfully")

def setup_out_dw(dw_name='./dw.db'):
    if os.path.exists(dw_name):
        os.remove(dw_name)

    dw_conn = sqlite3.connect(dw_name)
    dw_cur = dw_conn.cursor()

    # We make a table for each dimension and the FactTable
    dw_cur.executescript("""CREATE TABLE sales(
                            sale_ID INT,
                            office_ID INT,
                            sales_person_ID INT,
                            price INT,
                            currency TEXT,
                            PRIMARY KEY (sale_ID, office_ID, sales_person_ID)
                            );

                        CREATE TABLE office(
                            office_ID INT PRIMARY KEY,
                            location TEXT,
                            address TEXT
                            );

                        CREATE TABLE worker(
                            sales_person_ID INT,
                            name TEXT,
                            age INT,
                            contact TEXT,
                            position_ID,
                            PRIMARY KEY(sales_person_ID, position_ID)
                            );

                        CREATE TABLE worker_position(
                            position_ID INT PRIMARY KEY,
                            name TEXT,
                            salary INT
                            );



                            """)

    dw_conn.commit()
    dw_conn.close()
    print("Operation done successfully")

DB_NAME = './db.db'
DW_NAME = './dw.db'
setup_in_db(DB_NAME)
setup_out_dw(DW_NAME)
db_conn = sqlite3.connect(DB_NAME)
dw_conn = sqlite3.connect(DW_NAME)
dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)
NAME_MAPPING = ("sale_ID, price, currency, location, address, name, age, contact, position_name, " +
                "description, salary")
sales_source = SQLSource(connection=db_conn, query="SELECT * FROM sales", names=NAME_MAPPING)

fact_table = FactTable(
    name='factTable',
    keyrefs=['sale_ID', 'office_ID', 'sales_person_ID'],
    measures=['sale'])

office_dimension = Dimension(
    name='officeDim',
    key='office_ID',
    attributes=['location', 'address'])

worker_dimension = Dimension(
    name='workerDim',
    key='sales_person_ID',
    keyrefs='position_ID',


                            sales_person_ID INT,
                            name TEXT,
                            age INT,
                            contact TEXT,
                            position_ID,
)

# We create and object for each dimension in the DW and the FactTable
book_dimension = Dimension(
    name='bookDim',
    key='bookid',
    attributes=['book', 'genre'])

time_dimension = Dimension(
    name='timeDim',
    key='timeid',
    attributes=['day', 'month', 'year'])

location_dimension = Dimension(
    name='locationDim',
    key='locationid',
    attributes=['city', 'region'],
    lookupatts=['city'])

fact_table = FactTable(
    name='factTable',
    keyrefs=['bookid', 'locationid', 'timeid'],
    measures=['sale'])
