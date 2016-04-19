__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from itertools import filterfalse
from .predicate import Predicate
from .predicate_report import Report


class CompareTablePredicate(Predicate):
    def __init__(self, dw_table_name, test_table_name
                 , ignore_att = None, sort_att = None, subset = False):
        # TODO: The three last parameters still need to be implemented
        """
        :param dw_table: name of the table from dw to compare with
        :param test_table: list of dicts for table to compare against
        :param ignore_att: list of attributes that we wish to ignore
        :param sort_att: list of attributes for sorting tables before compare
        :param subset: indicates whether to compare with subset or not
        """

        # Fetching the DW table through its name
        self.dw_table_name = dw_table_name
        self.dw_table = []
        self.test_table_name = test_table_name
        self.test_table = []
        self.dw_surplus = None
        self.test_surplus = None

    def run(self, dw_rep):
        """
        Compares the two tables and sets their surpluses for reporting.
        """

        for entry in (dw_rep.get_data_representation(self.dw_table_name)):
            self.dw_table.append(entry)

        for entry in (dw_rep.get_data_representation(self.test_table_name)):
            self.test_table.append(entry)

        self.dw_surplus = \
            list(filterfalse(lambda x: x in self.dw_table, self.test_table))
        self.test_surplus = \
            list(filterfalse(lambda x: x in self.test_table, self.dw_table))

        # If both surplus lists are empty, each tuple has a match
        if len(self.dw_surplus) == 0 and len(self.test_surplus) == 0:
            self.__result__ = True
        else:
            self.__result__ = False

    def report(self):
        """
        Reports results of tests.
        If it fails it will print tuples with no match.
        """

        return Report(self.__class__.__name__,
                      self.__result__
                      )