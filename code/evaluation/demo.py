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


# Uden fejl
ndrp_test = NoDuplicateRowPredicate(table_name='authordim',
                                    column_names=['aid'],
                                    column_names_exclude=True)

# Med fejl
e_ndrp_test = NoDuplicateRowPredicate(table_name='authordim',
                                    column_names=['city', 'aid'],
                                    column_names_exclude=True)

# Uden fejl
fdp_test = FunctionalDependencyPredicate(table_name=['authordim', 'countrydim'],
                                         alpha='city',
                                         beta='country')

# Med fejl
e_fdp_test = FunctionalDependencyPredicate(table_name=['authordim', 'countrydim'],
                                         alpha='country',
                                         beta='city')

rip_test = ReferentialIntegrityPredicate()





pred_list = [ndrp_test, e_ndrp_test, fdp_test, e_fdp_test, rip_test]

dw_path = './dw.db'
pygrametl_program_path = './etl.py'
dwp = DWPopulator(pygrametl_program_path,
                  pep249_module=sqlite3,
                  program_is_path=True,
                  database=dw_path) # Arg til sqlite3

dw_rep = dwp.run()

# Checking how long it took.
time_before_test = time_passed(start)

case = Case(dw_rep, pred_list)

case.run()


time_after_test = time_passed(start)

# Checking how long it took.
print(" TIME BEFORE TEST " + time_before_test)
print(" TIME AFTER TEST " + time_after_test)
