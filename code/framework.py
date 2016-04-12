__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg & Arash Michael Sami Kjær'

import sqlite3
import os
from pygrametl_reinterpreter import *

class Framework:
    """
    Framework for running tests on a pygrametl program given a set of sources
    """

    def __init__(self, path, mapping, pred_list):
        """

        :param path:
        :param mapping:
        :param pred_list:
        :return:
        """
        self.path = path
        self.mapping = mapping
        self.pred_list = pred_list
        tc = Reinterpreter(self.path, self.mapping)
        self.dw_rep = tc.run()
        self.result_list = []

        for p in self.pred_list:
            p.run(self.dw_rep)
            report = p.report()
            report.run()


program_path = 'sample_program.py'

if os.path.isfile('a.db'):
    os.remove('a.db')
    conn1 = sqlite3.connect('a.db')
else:
    conn1 = sqlite3.connect('a.db')

if os.path.isfile('b.db'):
    os.remove('b.db')
    conn2 = sqlite3.connect('b.db')
else:
    conn2 = sqlite3.connect('b.db')

c = conn1.cursor()
c.execute('''CREATE TABLE DB (DIM1 INTEGER);''')

DB_info = [(1,), (2,), (3,)]
c.executemany("INSERT INTO DB(DIM1) VALUES (?);", DB_info)
conn1.commit()

c = conn2.cursor()
c.execute("CREATE TABLE DIM1 (key1 INTEGER PRIMARY KEY, attr1 TEXT, attr2 TEXT)")
c.execute("CREATE TABLE DIM2 (key2 INTEGER PRIMARY KEY, attr3 TEXT, attr4 TEXT)")
c.execute("CREATE TABLE FT1 (key1 INTEGER)")
conn2.commit()

conn_dict  = {'conn1': conn1, 'conn2': conn2}

tc = Reinterpreter(program=program_path, conn_scope=conn_dict, program_is_path=True)
scope = tc.run()








