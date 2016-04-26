__author__ = 'Alexander'
" This program is nice. I like it"

import pygrametl
from pygrametl.datasources import SQLSource, TypedCSVSource, CSVSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_csv = 'input.csv'
input2_csv = 'input2.csv'
output_conn = sqlite3.connect('dw.db')

input_src = TypedCSVSource(input_csv, {})
input2_src = CSVSource(input2_csv)
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

dim1 = Dimension(
    'dim1',
    'key1',
    ['attr1', 'attr2']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr3', 'attr4'],
)

ft1 = FactTable(
    name='ft1',
    keyrefs=['key1']
)

output_conn.close()
