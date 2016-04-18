import sys
sys.path.append('../')
sys.path.append('../../')
import sqlite3
from row_number_predicate import RowPredicate
from datwarehouse_representation import DWRepresentation, DimRepresentation, FTRepresentation


dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

f =  FTRepresentation('factTable', ['bookid','locationid','timeid'],['sale'], dw_conn)
b = DimRepresentation('bookDim', 'bookid', ['genre'], ['book'], dw_conn)
l = DimRepresentation('locationDim', 'locationid', ['region'], ['city'], dw_conn)
t = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'], [], dw_conn)
Big = DWRepresentation([b,l,t],[f],dw_conn)

RowTest = RowPredicate(Big, 'factTable', 4)

RowTest.run()
RowTest.report()

