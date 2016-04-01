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
ref_tester = ReferentialPredicate(dic)
ref_tester.run(fact_table, 'book', 'bookid')
ref_tester.run('book', fact_table, 'bookid')
ref_tester.run(fact_table, 'location', 'locationid')
ref_tester.run('location', fact_table, 'locationid')
ref_tester.run(fact_table, 'time', 'timeid')
ref_tester.run('time', fact_table, 'timeid')