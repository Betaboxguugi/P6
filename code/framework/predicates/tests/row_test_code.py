__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

import sqlite3
from framework.predicates import RowCountPredicate
from framework.reinterpreter.datawarehouse_representation import \
    DWRepresentation, DimRepresentation, FTRepresentation

dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn)
time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'],
                             dw_conn)
location_dim = DimRepresentation('locationDim', 'locationid',
                                 ['city', 'region'], dw_conn, ['city'])
facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'],
                             dw_conn, ['sale'])
dw = DWRepresentation([book_dim, time_dim, location_dim],  dw_conn,
                      [facttable])

RowTest = RowCountPredicate('factTable', 5)

print(RowTest.run(dw))

