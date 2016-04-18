__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

import sys
sys.path.append('../')
sys.path.append('../../')
import sqlite3
from referential_integrity_predicate import ReferentialPredicate
from datwarehouse_representation import DWRepresentation, DimRepresentation, FTRepresentation


dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)
query1 = "SELECT * FROM bookDim WHERE bookid > 1"
query2 = "SELECT * FROM factTable WHERE timeid < 1"
book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn, query=query1)
time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'], dw_conn)
location_dim = DimRepresentation('locationDim', 'locationid', ['city', 'region'], dw_conn, ['city'])
facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'], ['sale'], dw_conn, query=query2)
dw = DWRepresentation([book_dim, time_dim, location_dim], [facttable], dw_conn)

ref_tester = ReferentialPredicate()
ref_tester.run(dw)
report = ref_tester.report()
report.run()
