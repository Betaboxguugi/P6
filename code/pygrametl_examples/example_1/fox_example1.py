"""My own little test place, figuring out pygrametl"""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sys
import os.path
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import Dimension, FactTable
from pygrametl.steps import *
import sqlite3
from db_1 import setup_input_db, setup_out_dw, setup_input_csv
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

dw_name = './dw.db'

if os.path.exists(dw_name):
    os.remove(dw_name)

dw_conn = sqlite3.connect(dw_name)
dw_cur = dw_conn.cursor()

# We make a table for each dimension and the FactTable
dw_cur.executescript("""CREATE TABLE sales(
                            sale_ID INT,
                            office_ID INT,
                            sales_person_ID INT,
                            product_ID INT,
                            date_ID INT,
                            supplier_id INT,
                            price INT,
                            currency INT,
                            PRIMARY KEY (sale_ID, office_ID, sales_person_ID, product_ID, date_ID, supplier_id)
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
                            description TEXT,
                            salary INT
                            );



                            """)
dw_conn.commit()
dw_conn.close()

print("Operation done successfully")
conn.commit()
conn.close()
