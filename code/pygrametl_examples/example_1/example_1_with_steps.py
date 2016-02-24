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
from pygrametl.steps import *
import sqlite3
from db_1 import setup_input_db, setup_out_dw, setup_input_csv
from step_funcs import *


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

# We put the regions into our location_dimension
[location_dimension.insert(row) for row in region_source]
csv_file_handle.close()

a = [('genre', cookbook_fix)]
s = MappingStep(a)

step_starter = SourceStep(sales_source)
time_splitter = Step(split_timestamp)
printer = PrintStep()
ensure_book = DimensionStep(dimension=book_dimension, keyfield='bookid')
ensure_time = DimensionStep(dimension=time_dimension, keyfield='timeid')
ensure_location = DimensionStep(dimension=location_dimension, keyfield='locationid')
ft_insert = Step(fact_table.insert)

connectsteps(step_starter, time_splitter, ensure_book, ensure_time, ensure_location, ft_insert, printer)
step_starter.start()

dw_conn_wrapper.commit()
dw_conn_wrapper.close()

sales_conn.close()