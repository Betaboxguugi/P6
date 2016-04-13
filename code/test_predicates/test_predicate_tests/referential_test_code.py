import sqlite3
from test_predicates.referential_integrity_predicate import ReferentialPredicate
from pygrametl.datasources import SQLSource


dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)
fact_table = 'sales'
keys = ['bookid', 'timeid', 'locationid']
dic = dict()
dic[fact_table] = SQLSource(connection=dw_conn, query="SELECT * FROM factTable")
dic['book'] = SQLSource(connection=dw_conn, query="SELECT * FROM bookDim WHERE bookid > 1")
dic['location'] = SQLSource(connection=dw_conn, query="SELECT * FROM locationDim")
dic['time'] = SQLSource(connection=dw_conn, query="SELECT * FROM timeDim")

aa = DimRepresentation('factTable', 'ID', ['AGE', 'ADDRESS', 'SALARY'], ['NAME'], conn)  # TODO Fix all this shit
bb = FTRepresentation('BOMPANY', ['NAME', 'ADDRESS', 'ID'], ['AGE', 'SALARY'], conn)
cc = DWRepresentation([aa], [bb], conn)

ref_tester = ReferentialPredicate(dic, fact_table, 'book', 'bookid')
ref_tester2 = ReferentialPredicate(dic, fact_table, 'location', 'locationid')
ref_tester3 = ReferentialPredicate(dic, fact_table, 'time', 'timeid')
ref_tester.run()
ref_tester2.run()
ref_tester3.run()
