__author__ = 'Alexander'

from reinterpreter import Reinterpreter
import sqlite3

DB = 'brandtest.db'
DW = 'dwtest.db'
CSV = 'weapontest.csv''

program_path = 'brand_sample.py'

setup_input_db(DB)
setup_out_dw(DW)
setup_input_csv(CSV)

db_conn = sqlite3.connect(DB)
dw_conn = sqlite3.connect(DW)
csv_conn = sqlite3.connect(CSV)

conn_dict  = {'conn1': db_conn, 'conn2': dw_conn, 'conn4': csv_conn}

tc = Reinterpreter(program=program_path, conn_scope=conn_dict, program_is_path=True)
scope = tc.run()


def close():
    conn1.close()
    conn2.close()

globals().update({'close':close})
globals().update(scope)
