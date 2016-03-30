__author__ = 'Alexander'
import sys
sys.path.append('../')
from reinterpreter import Reinterpreter
from db_test_setup import *
import sqlite3

DB = './brandtest.db'
DW = './dwtest.db'
CSV = './weapontest.csv'

program_path = './brand_sample.py'

setup_input_db(DB)
setup_out_dw(DW)
# setup_input_csv(CSV)

db_conn = sqlite3.connect(DB)
dw_conn = sqlite3.connect(DW)


#csv_conn = sqlite3.connect(CSV)

conn_dict = {'conn0': dw_conn, 'conn1': db_conn}

try:
    tc = Reinterpreter(program=program_path, conn_scope=conn_dict, program_is_path=True)
    scope = tc.run()
finally:
    db_conn.close()
    dw_conn.close()
