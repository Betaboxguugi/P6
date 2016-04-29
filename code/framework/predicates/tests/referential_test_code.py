__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

import sqlite3
from framework.predicates.referential_integrity_predicate \
    import ReferentialIntegrityPredicate
from framework.reinterpreter.datawarehouse_representation \
    import DWRepresentation, DimRepresentation, FTRepresentation

csv_name = './region.csv'
dw_name = './dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

query1 = "SELECT * FROM bookDim WHERE bookid < 3"
query2 = "SELECT * FROM timeDim"
query3 = "SELECT * FROM locationDim"
query4 = "SELECT * FROM factTable WHERE bookid > 1"
book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn)

time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'],
                             dw_conn)

location_dim = DimRepresentation('locationDim', 'locationid',
                                 ['city', 'region'], dw_conn, ['city'])

facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'],
                             dw_conn, ['sale'])

book_dim.query = query1
time_dim.query = query2
location_dim.query = query3
facttable.query = query4

dw = DWRepresentation([book_dim, time_dim, location_dim], [facttable], dw_conn)

ref_tester = ReferentialIntegrityPredicate()
ref_tester.run(dw)
