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

ref_tester = ReferentialPredicate(dic, fact_table, 'book', 'bookid')
#ref_tester2 = ReferentialPredicate(dic, 'book', fact_table, 'bookid')
ref_tester3 = ReferentialPredicate(dic, fact_table, 'location', 'locationid')
#ref_tester4 = ReferentialPredicate(dic, 'location', fact_table, 'locationid')
ref_tester5 = ReferentialPredicate(dic, fact_table, 'time', 'timeid')
#ref_tester6 = ReferentialPredicate(dic, 'time', fact_table, 'timeid')

ref_tester.run()
#ref_tester2.run()
ref_tester3.run()
#ref_tester4.run()
ref_tester5.run()
#ref_tester6.run()
