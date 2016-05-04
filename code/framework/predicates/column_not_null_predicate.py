# IMPORTS
from .predicate import Predicate
from .predicate_report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class ColumnNotNullPredicate(Predicate):
    def __init__(self, table_name, column_names):
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_names: name of the specified column, which needs to be
        tested within the table
        :type column_names: list or str
        """
        self.table_name = table_name
        self.column_names = []
        self.rows_with_null = []

        if isinstance(column_names, str):
            self.column_names = [column_names]
        else:
            self.column_names = column_names

        # If else chain that insures column_names is either a list of strings
        # or a string
        if type(column_names) is list:
            for cn in range(0, len(column_names)):
                if not type(column_names[cn]) is str:
                    raise TypeError(
                        'column_names must be a list of strings or a string')
                self.column_names.append(column_names[cn])
        elif type(column_names) is str:
            self.column_names.append(column_names)
        else:
            raise TypeError(
                'column_names must be a list of strings or a string')

    def run(self, dw_rep):
        """
        Then checks each element in the specified column,
        if any are null, it sets self.__result__ to false. Finally calls
        self.report()
        """
        self.__result__ = True

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

