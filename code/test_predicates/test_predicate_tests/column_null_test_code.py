import sqlite3
from test_predicates.has_null import HasNull
from pygrametl.datasources import SQLSource

dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)
dic = dict()
dic['sales'] = SQLSource(connection=dw_conn, query="SELECT * FROM factTable")
dic['book'] = SQLSource(connection=dw_conn, query="SELECT * FROM bookDim")
dic['location'] = SQLSource(connection=dw_conn, query="SELECT * FROM locationDim")
dic['time'] = SQLSource(connection=dw_conn, query="SELECT * FROM timeDim")

constrain_tester1 = HasNull(dic, 'sales', 'sale')
constrain_tester2 = HasNull(dic, 'book', 'genre')


constrain_tester1.run()
constrain_tester2.run()