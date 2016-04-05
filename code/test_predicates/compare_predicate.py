__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'

import sqlite3
from pygrametl.datasources import *
import itertools
from test_predicates.t_predicate import TPredicate


class ComparePredicate(TPredicate):
    def __init__(self, dw_table, test_table, ignore_att = None, sort_att = None, subset = False):
        # TODO: The three last parameters still need to be implemented
        """
        :param dw_table: the table from dw that we wish to compare with
        :param test_table: user given table that we compare against
        The other parameters are not finished, but here are their descriptions
        :param ignore_att: attributes, such as keys, that we wish to ignore for the comparison
        :param sort_att: user given attributes used for sorting tables before compare
        :param subset: flag that indicates whether the test table should only be a subset of the dw table
        """

        # Creates the dw_table, a list of dicts.
        dw_dict = super(ComparePredicate, self).dictify(dw_table)
        self.dw_table = dw_dict[next(iter(dw_dict.keys()))]

        # Creates the test_table, a list of dicts.
        test_dict = super(ComparePredicate, self).dictify(test_table)
        self.test_table = test_dict[next(iter(test_dict.keys()))]

        self.dw_surplus = list(itertools.filterfalse(lambda x: x in self.dw_table, self.test_table))
        self.test_surplus = list(itertools.filterfalse(lambda x: x in self.test_table, self.dw_table))

        self.run()
        self.report()

    def run(self):
        """ Compares the two tables and sets their surpluses for reporting."""

        # If both surplus lists are empty, it means that each tuple has a match, and the test passes.
        if len(self.dw_surplus) == 0 and len(self.test_surplus) == 0:
            self.__result__ = True
        else:
            self.__result__ = False

    def report(self):
        """ Reports results of tests. If it fails it will print tuples with no match."""
        if self.__result__:
            print(self.__result__)
        else:
            print(self.__result__)
            print("Exclusive to dw:")
            print(self.dw_surplus)
            print("Exclusive to test:")
            print(self.test_surplus)

"""
dic = {}
dic2 = {}

SALES_DB_NAME = './sales.db'
DW_NAME = './dw.db'
CSV_NAME = './region.csv'
sales_conn = sqlite3.connect(SALES_DB_NAME)
csv_file_handle = open(CSV_NAME, "r")

dic['sales'] = SQLSource(connection=sales_conn, query="SELECT * FROM sales")
dic2['sal2s'] = SQLSource(connection=sales_conn, query="SELECT * FROM sales")

a = ComparePredicate(dw_table=dic, test_table=dic2)
"""