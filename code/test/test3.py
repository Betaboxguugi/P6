__author__ = 'Alexander'
import sys
sys.path.append('../')
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
import  sqlite3
import os

SALES_DB_NAME = './2sales.db'
DW_NAME = './2dw.db'
CSV_NAME = './2region.csv'
path = "C:/Users/Alexander/Documents/GitHub/P6/code/examples/pygrametl" \
"_examples/example_1/example_1.py"

s1 = sqlite3.connect(SALES_DB_NAME)
s2 = open(CSV_NAME, "r")

n = ColumnNotNullPredicate('bookdim', 'bookid')

c = Case(path, [s1, s2], [n], True, sqlite3, database=DW_NAME)
c.run()