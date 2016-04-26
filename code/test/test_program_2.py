__author__ = 'Alexander'
"User forgets to declare dimensions and fact tables "

import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_conn = sqlite3.connect('input.db')
input2_conn = sqlite3.connect('input2.db')
output_conn = sqlite3.connect('dw.db')

input_src = SQLSource(input_conn, query='SELECT * FROM table')
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

input_conn.close()
output_conn.close()