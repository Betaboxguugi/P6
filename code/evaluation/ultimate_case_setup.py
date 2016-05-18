from framework.case import Case
from framework.dw_populator import DWPopulator
from framework.predicates import *
import sqlite3
import time

start = time.monotonic()

def time_passed(start):
    end = time.monotonic()
    elapsed = end - start
    return '{}{}'.format(round(elapsed, 3), 's')

def constraint_row(a):
    if a > 2012:
        return False
    else:
        return True

def constraint_column(a, b):
    if len(a) > len(set(a)):
        return False
    elif len(b) > len(set(b)):
        return False
    else:
        return True

table1 = 'authordim'
table2 = 'bookdim'
table3 = 'countrydim'
fact_table = 'facttable'

cnnp_test = ColumnNotNullPredicate(table1)
ctp_test = CompareTablePredicate(table2, table2)
fdp_test = FunctionalDependencyPredicate([table1, table3], 'cid', 'city')
ndrp_test = NoDuplicateRowPredicate(table1, ['city', 'aid'], True)
rip_test = ReferentialIntegrityPredicate()
rocp_test = RowCountPredicate(table2, 6)
rucp_test = RuleColumnPredicate(table1, constraint_column, ['name', 'city'])
rrp_test = RuleRowPredicate(table2, constraint_row, ['year'])
scdvp_test = SCDVersionPredicate(table2, {"title": 'EZ PZ ETL'}, 4)

pred_list = [cnnp_test, ctp_test, fdp_test, ndrp_test, rip_test, rocp_test, rucp_test,
             rrp_test, scdvp_test]

dw_path = './dw.db'
pygrametl_program_path = './etl.py'
dwp = DWPopulator(pygrametl_program_path, sqlite3, True, database=dw_path)

dw_rep = dwp.run()

case = Case(dw_rep, pred_list)

case.run()
print(time_passed(start))