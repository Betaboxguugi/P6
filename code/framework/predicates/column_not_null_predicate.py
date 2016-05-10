# IMPORTS
from .predicate import Predicate
from .report import Report
import time

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class ColumnNotNullPredicate(Predicate):
    def __init__(self, table_name, column_names=None,
                 column_names_exclude=False):
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_names: name of the specified column, which needs to be
        tested within the table
        :type column_names: list or str
        """
        self.table_name = table_name
        self.rows_with_null = []
        self.column_names = column_names
        self.column_names_exclude = column_names_exclude

    def run(self, dw_rep):
        """
        :param dw_rep
        Then checks each element in the specified column,
        if any are null, it sets self.__result__ to false. Finally calls
        self.report()
        """
        self.__result__ = True
        self.setup_columns(dw_rep)
        for row in dw_rep.get_data_representation(self.table_name):
            if None in row.values():
                self.rows_with_null.append(row)
        if self.rows_with_null:
            self.__result__ = False

        return Report(result=self.__result__,
                      predicate=self,
                      tables=self.table_name,
                      elements=self.rows_with_null,
                      msg=None)
