# IMPORTS
from .predicate import Predicate
from .report import Report
import time

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class ColumnNotNullPredicate(Predicate):
    """
    Predicate for asserting that nulls do not exist in the columns of a table
    """

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
        Iterates over the table, storing any row containing nulls.
        :param dw_rep : DWRepresentation object
        """

        # Gets the columns to iterate over
        chosen_columns = self.setup_columns(dw_rep,self.table_name,
                                            self.column_names,
                                            self.column_names_exclude)

        # Iterates over the table and checks for nulls in chosen columns
        table = dw_rep.get_data_representation(self.table_name)
        for row in table.itercolumns(chosen_columns):
            if None in row.values():
                self.rows_with_null.append(row)

        if not self.rows_with_null:
            self.__result__ = True

        return Report(result=self.__result__,
                      predicate=self,
                      tables=self.table_name,
                      elements=self.rows_with_null,
                      msg=None)
