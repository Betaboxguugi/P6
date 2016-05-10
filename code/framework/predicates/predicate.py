__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from pygrametl.datasources import *
from csv import DictReader


class Predicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def run(self, *args):
        """ Runs the actual test. Stores result in __result__"""
        self.__result__ = True

    def setup_columns(self, dw_rep):
        # setup of columns, if column_names_exclude is true, then columns is
        # all other columns than the one(s) specified.
        if not self.column_names and not self.column_names_exclude:
            self.column_names_exclude = True
        # We can't iterate over a string so we convert self.column_names
        # into a list if necessary.
        if isinstance(self.column_names, str):
            self.column_names = [self.column_names]
        if self.column_names_exclude:
            temp_columns_list = []
            for column in dw_rep.get_data_representation(self.table_name).all:
                temp_columns_list.append(column)
            if self.column_names:
                for column_name in self.column_names:
                    temp_columns_list.remove(column_name)
            self.column_names = temp_columns_list

    def report(self):
        """
        returns the result of the test
        """

