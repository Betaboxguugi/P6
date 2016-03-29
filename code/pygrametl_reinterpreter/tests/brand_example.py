__author__ = 'Alexander'

from reinterpreter import Reinterpreter
import sqlite3

program_path = 'brand_sample.py'

conn1 = sqlite3.connect('a.db')


conn_dict  = {'conn1': conn1, 'conn2': conn2}

tc = Reinterpreter(program=program_path, conn_scope=conn_dict, program_is_path=True)
scope = tc.run()


def close():
    conn1.close()
    conn2.close()

globals().update({'close':close})
globals().update(scope)
