__author__ = 'Alexander'
" User gives connections directly to pygrametl objects. Not as variables."

import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_src = SQLSource(sqlite3.connect('input.db'), query='SELECT * FROM table')
input2_src = SQLSource(sqlite3.connect('input2.db'), query='SELECT * FROM table')
output_wrapper = pygrametl.ConnectionWrappersqlite3.connect('output.db')

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
