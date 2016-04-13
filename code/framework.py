__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg & Arash Michael Sami Kjær'

import sqlite3
import os
from pygrametl_reinterpreter import *
from test_predicates import *
from pygrametl_reinterpreter.tests.reinterpreterMockup import ReinterpreterMockup
from test_predicates.row_number_predicate import RowPredicate

class Framework:
    """
    Framework for running predicate tests on a pygrametl program given a set of sources
    """

    def __init__(self, program, mapping, pred_list, program_is_path):
        """
        :param program: A path or string of a pygrametl program
        :param mapping: A map of sources
        :param pred_list: A list of predicates we wish to run
        """
        self.program = program
        self.mapping = mapping
        self.pred_list = pred_list
        self.program_is_path = program_is_path

        # Sets up and runs reinterpreter getting DWRepresentation object
        tc = ReinterpreterMockup()
            #Reinterpreter(program=self.program, conn_scope=self.mapping, program_is_path = self.program_is_path)
        self.dw_rep = tc.run()

        # Runs all predicates and reports their results
        for p in self.pred_list:
            p.run(self.dw_rep)
            report = p.report()
            report.run()

rowp = RowPredicate('company', 5)
pl = [rowp]
framework = Framework(None, None, pl, None)


"""
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

a = RowPredicate('DIM1', 0)
Framework(program_path, conn_dict, [a], True)
"""






