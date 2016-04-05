""" This is an implementaion of the get started tutorial from pygrametl.org, but using SQLite as our
DBMS instead of PostgreSQL. This example will be reliant on some databases already being set up
earlier. These databases can be created with the python script, db_1.py.
"""
__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'

# IMPORTS
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import Dimension, FactTable
import sqlite3
from db_1 import setup_input_db, setup_out_dw, setup_input_csv

# CONSTANTS
SALES_DB_NAME = './sales.db'
DW_NAME = './dw.db'
CSV_NAME = './region.csv'
NAME_MAPPING = 'saleid', 'book', 'genre', 'city', 'timestamp', 'sale'



# First we set up the DBs and CSV file
setup_input_db(SALES_DB_NAME)
setup_input_csv(CSV_NAME)
setup_out_dw(DW_NAME)

# We then connect to these DBs
sales_conn = sqlite3.connect(SALES_DB_NAME)
dw_conn = sqlite3.connect(DW_NAME)

# Wrapper for pygrametl, so that it now is in charge of our DW stuff
dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)

# We make a source for our SQL and CSV
# NOTE: We use NAME_MAPPING to do some mapping for us, not sure why.
sales_source = SQLSource(connection=sales_conn, query="SELECT * FROM sales", names=NAME_MAPPING) 

csv_file_handle = open(CSV_NAME, "r")
region_source = CSVSource(f=csv_file_handle, delimiter=',')

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


# NOTE: Most of the following code is taken directly form pygrametl.org and has little to do with
# making this example portable to SQLite and this particular implementation. It is however down here
# that a lot of the cool stuff happens, i.e. the ETL stuff.
# Python function needed to split the timestamp into its three parts
def split_timestamp(row):
    """Splits a timestamp containing a date into its three parts
    """

    # Splitting of the timestamp into parts
    timestamp = row['timestamp']
    timestamp_split = timestamp.split('/')

    # Assignment of each part to the dictionary
    row['year'] = timestamp_split[0]
    row['month'] = timestamp_split[1]
    row['day'] = timestamp_split[2]

# We put the regions into our location_dimension
[location_dimension.insert(row) for row in region_source]
csv_file_handle.close()

# Each row in the sales database is iterated through and inserted
for row in sales_source:

    # Each row is passed to the timestamp split function for splitting
    split_timestamp(row)

    # Lookups are performed to find the key in each dimension for the fact
    # and if the data is not there, it is inserted from the sales row
    row['bookid'] = book_dimension.ensure(row)
    row['timeid'] = time_dimension.ensure(row)

    # For the location dimension, all the data is already present, so a
    # missing row must be an error
    row['locationid'] = location_dimension.lookup(row)
    if not row['locationid']:
       raise ValueError("city was not present in the location dimension")

    # The row can then be inserted into the fact table
    fact_table.insert(row)

# The data warehouse connection is then ordered to commit and close
dw_conn_wrapper.commit()
dw_conn_wrapper.close()

sales_conn.close()
