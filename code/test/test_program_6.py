__author__ = 'Alexander'
" User decides to interact with source before declaring as a data source"

import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_conn = sqlite3.connect('input.db')
input2_conn = sqlite3.connect('input2.db')
output_conn = sqlite3.connect('output.db')

a = input_conn.cursor()
a.execute("INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);")

input_src = SQLSource(input_conn, query='SELECT * FROM table')
input2_src = SQLSource(input2_conn, query='SELECT * FROM table')
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

dim1 = Dimension(
    'dim1',
    'key1',
    ['attr1', 'attr2']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr3', 'attr4']
)

ft1 = FactTable(
    name='ft1',
    keyrefs=['key1']
)

input_conn.close()
output_conn.close()
