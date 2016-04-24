__author__ = 'Alexander'
" User does not use sources"

import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

output_conn = sqlite3.connect('output.db')

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

