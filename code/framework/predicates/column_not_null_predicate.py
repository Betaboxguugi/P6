# IMPORTS
from .predicate import Predicate
from .report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class ColumnNotNullPredicate(Predicate):
    def __init__(self, table_name, column_names=None, column_names_exclude=False):
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

    def run(self, dw_rep):
        """
        Then checks each element in the specified column,
        if any are null, it sets self.__result__ to false. Finally calls
        self.report()
        """
        self.__result__ = True
        self.setup_columns(dw_rep)

        for row in dw_rep.get_data_representation(self.table_name):
            e = []  # list of elements
            for column_name in self.column_names:
                e.append(row.get(column_name))
            if None in e:
                self.rows_with_null.append(row)
        if self.rows_with_null:
            self.__result__ = False

        return self.report()

    def report(self):
        """
        If null is found, prints what table and column null resides in,
        otherwise prints true
        """
        return Report(self.__result__,
                      self.__class__.__name__,
                      self.rows_with_null,
                      'at rows {}'.format(self.rows_with_null)
                      )

