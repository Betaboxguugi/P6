__author__ = 'Alexander'
import sys
sys.path.append('../')
from framework.case import Case
from framework.dw_populator import DWPopulator
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
from framework.predicates import RowCountPredicate
import  sqlite3
import os

SALES_DB_NAME = './2sales.db'
DW_NAME = "C:/Users/Alexander/Documents/GitHub/P6/code/examples/pygrametl" \
"_examples/example_1/dw.db"
CSV_NAME = './2region.csv'
path = "C:/Users/Alexander/Documents/GitHub/P6/code/examples/pygrametl" \
"_examples/example_1/example_1.py"

s1 = sqlite3.connect(SALES_DB_NAME)
s2 = open(CSV_NAME, "r")
n = RowCountPredicate('bookdim', 1)


dwp = DWPopulator(path, sqlite3, True, database=DW_NAME)
rep = dwp.run()

c = Case(rep, [n])
c.run()
