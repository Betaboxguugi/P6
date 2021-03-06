import sys
sys.path.append('../')
from framework.case import Case
from framework.dw_populator import DWPopulator
from framework.predicates import *
import sqlite3
import time

start = time.monotonic()

def time_passed(start_time):
    end = time.monotonic()
    elapsed = end - start_time
    return '{}{}'.format(round(elapsed, 3), 's')

table1 = 'authordim'
table2 = 'bookdim'
table3 = 'countrydim'
fact_table = 'facttable'
goodbooks = 'goodbooksdim'

cnnp_test = ColumnNotNullPredicate(table1)
ctp_test = CompareTablePredicate(table2, goodbooks, ['ID'], True, False, (), True, True)
fdp_test = FunctionalDependencyPredicate([table1, table3], 'cid', 'city')
ndrp_test = NoDuplicateRowPredicate(table1, ['city', 'aid'], True)
rip_test = ReferentialIntegrityPredicate()
rocp_test = RowCountPredicate(table2, 6)
scdvp_test = SCDVersionPredicate(table2, {"title": 'EZ PZ ETL'}, 4)

pred_list = [cnnp_test, ctp_test, fdp_test, ndrp_test, rip_test, rocp_test,
             scdvp_test]

dw_path = './dw.db'
pygrametl_program_path = './etl.py'
dwp = DWPopulator(pygrametl_program_path, sqlite3, True, database=dw_path)

dw_rep = dwp.run()

# Checking how long it took.
time_before_test = time_passed(start)

case = Case(dw_rep, pred_list)

case.run()


time_after_test = time_passed(start)

# Checking how long it took.
print(" TIME BEFORE TEST " + time_before_test)
print(" TIME AFTER TEST " + time_after_test)
