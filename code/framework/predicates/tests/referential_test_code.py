__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

import sqlite3
from framework.predicates.referential_integrity_predicate \
    import ReferentialPredicate
from framework.reinterpreter.datawarehouse_representation \
    import DWRepresentation, DimRepresentation, FTRepresentation

csv_name = './region.csv'
dw_name = './dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

query1 = "SELECT * FROM bookDim"
query2 = "SELECT * FROM timeDim"
query3 = "SELECT * FROM locationDim"
query4 = "SELECT * FROM factTable"
book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn,
                             query=query1)

time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'],
                             dw_conn, query=query2)

location_dim = DimRepresentation('locationDim', 'locationid',
                                 ['city', 'region'], dw_conn, ['city'],
                                 query=query3)

facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'],
                             ['sale'], dw_conn, query=query4)

dw = DWRepresentation([book_dim, time_dim, location_dim], [facttable], dw_conn)

ref_tester = ReferentialPredicate()
ref_tester.run(dw)
report = ref_tester.report()  # Not testing using the framework,
report.run()                  # so it looks ugly this way
