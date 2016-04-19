__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
import itertools
from .predicate import Predicate
from .predicate_report import Report


class CompareTablePredicate(Predicate):
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