
import sys
sys.path.append('../../../')
from framework.predicates import NotNull
import framework


import sqlite3
from pygrametl.datasources import SQLSource

dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)
dic = dict()
dic['sales'] = SQLSource(connection=dw_conn, query="SELECT * FROM factTable")
dic['book'] = SQLSource(connection=dw_conn, query="SELECT * FROM bookDim")
dic['location'] = SQLSource(connection=dw_conn, query="SELECT * FROM locationDim")
dic['time'] = SQLSource(connection=dw_conn, query="SELECT * FROM timeDim")

constrain_tester1 = NotNull('sales', 'sale')
constrain_tester2 = NotNull('book', 'genre')

framework.Case(None, None, [NotNull], True)


constrain_tester1.run()
constrain_tester2.run()
