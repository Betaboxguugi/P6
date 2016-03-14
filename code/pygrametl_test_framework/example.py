""" An example of how to run a test
"""

__author__ = 'Mathias Claus Jensen'

from test_class import TestClass
import sqlite3

program_path = 'sample_program.py'

conn1 = sqlite3.connect('a.db')
conn2 = sqlite3.connect('b.db')


conn_dict  = {'conn1': conn1, 'conn2': conn2}
    
tc = TestClass(conn_map=conn_dict, program_path=program_path, predicates=None)
tc.run()
