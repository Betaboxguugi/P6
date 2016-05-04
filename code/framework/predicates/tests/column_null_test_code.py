from framework.reinterpreter.datawarehouse_representation \
    import DWRepresentation, DimRepresentation, FTRepresentation
from framework.predicates.column_not_null_predicate import \
    ColumnNotNullPredicate
import sqlite3

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn)

time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'],
                             dw_conn)

location_dim = DimRepresentation('locationDim', 'locationid',
                                 ['city', 'region'], dw_conn, ['city'])

facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'],
                             dw_conn, ['sale'])
dw = DWRepresentation([book_dim, time_dim, location_dim], dw_conn, [facttable])

notnull_tester1 = ColumnNotNullPredicate('sales', 'sale')
notnull_tester2 = ColumnNotNullPredicate('book', 'genre')

print(notnull_tester1.run(dw))
print(notnull_tester2.run(dw))
