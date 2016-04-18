import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3


input_conn = sqlite3.connect('input.db')
output_conn = sqlite3.connect('output.db')

input_src = SQLSource(input_conn, query='SQL CODE BIATCH')
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

dim1 = Dimension(
    name='name1',
    key='key1',
    attributes=['attr1', 'attr2']
)

ft1 = FactTable(
    name='factTable',
    keyrefs=['key1',]
)
