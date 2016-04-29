__author__ = 'Alexander'
" This script is made as a hub to test various things about the reinterpreter "
" We want to tests its limits. What can it do? What is it unable to do?"

import sys
sys.path.append('../')
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
import  sqlite3

path = "test_program_1.py"


notnull = ColumnNotNullPredicate('dim1', 'att1')



input_conn = sqlite3.connect('input.db')
input2_conn = sqlite3.connect('input2.db')


dw_conn = sqlite3.connect('dw.db')
dw_conn2 = sqlite3.connect('dw2.db')


try:
    # Exact amount of sources
    c = Case(path, [input_conn, input2_conn], dw_conn, [notnull], True)
    c.run()
except Exception as e:
    print(e)

try:
    # Exact amount of sources
    c = Case(path, [input_conn, input2_conn], dw_conn2, [notnull], True)
    c.run()
except Exception as e:
    print(e)
