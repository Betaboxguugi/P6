__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
import os
import sqlite3
import sys
sys.path.append('../')
import sqlite3
from pygrametl.datasources import *
import itertools
from test_predicates.t_predicate import TPredicate
from .report import Report
from pygrametl_reinterpreter import *


class ComparePredicate(TPredicate):
    def __init__(self, dw_table_name, test_table_name, ignore_att = None, sort_att = None, subset = False):
        # TODO: The three last parameters still need to be implemented
        """
        :param dw_table: name of the table from dw that we wish to compare with
        :param test_table: list of dicts representing table we wish to compare against
        The other parameters are not finished, but here are their descriptions
        :param ignore_att: attributes, such as keys, that we wish to ignore for the comparison
        :param sort_att: user given attributes used for sorting tables before compare
        :param subset: flag that indicates whether the test table should only be a subset of the dw table
        """

        # Fetching the DW table through its name
        self.dw_table_name = dw_table_name
        self.dw_table = []
        self.test_table_name = test_table_name
        self.test_table = []
        self.dw_surplus = None
        self.test_surplus = None

    def run(self, dw_rep):
        """ Compares the two tables and sets their surpluses for reporting."""

        for entry in (dw_rep.get_data_representation(self.dw_table_name)):
            self.dw_table.append(entry)

        for entry in (dw_rep.get_data_representation(self.test_table_name)):
            self.test_table.append(entry)

        self.dw_surplus = list(itertools.filterfalse(lambda x: x in self.dw_table, self.test_table))
        self.test_surplus = list(itertools.filterfalse(lambda x: x in self.test_table, self.dw_table))

        # If both surplus lists are empty, it means that each tuple has a match, and the test passes.
        if len(self.dw_surplus) == 0 and len(self.test_surplus) == 0:
            self.__result__ = True
        else:
            self.__result__ = False

    def report(self):
        """ Reports results of tests. If it fails it will print tuples with no match."""

        return Report(self.__class__.__name__,
                      self.__result__
                      )

    """if self.__result__:
        print(self.__result__)
    else:
        print(self.__result__)
        print("Exclusive to dw:")
        print(self.dw_surplus)
        print("Exclusive to test:")
        print(self.test_surplus)
    """



"""
# Ensures a fresh database to work with.
TEST_DB = 'test.db'
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

conn = sqlite3.connect(TEST_DB)
c = conn.cursor()

# Making table to test on...
c.execute('''CREATE TABLE COMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')

company_info = [('Anders', 43, 'Denmark', 21000.00),
                ('CharLes', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Swedden', 19000.00),
                ('Hannibal', 45, 'Amerrica', 65000.00),
                ('Buggy Bug', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

a = DimRepresentation('COMPANY', 'ID', ['AGE', 'ADDRESS', 'SALARY'], ['NAME'], conn)
b = FTRepresentation('BOMPANY', ['NAME', 'ADDRESS', 'ID'], ['AGE', 'SALARY'], conn)
Big = DWRepresentation([a], [b], conn)

test_entries = []
for entry in (Big.get_data_representation('COMPANY')):
    test_entries.append(entry)
test_entries.append(4)

a = ComparePredicate(dw_table='COMPANY', test_table=test_entries)
a.run()
a.report()
"""