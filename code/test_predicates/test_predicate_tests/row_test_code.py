import os
import sqlite3
from pygrametl.datasources import SQLSource
import sys
sys.path.append('../')
from  row_number_predicate import *
sys.path.append('../../')
from pygrametl_reinterpreter import *


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

