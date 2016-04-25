import inspect
from .predicate import Predicate
from .predicate_report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class RulePredicate(Predicate):
    def __init__(self, table_name, constraint_function, column_name=None,
                 column_names=None, return_list=None):
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_name: name of the specified column, which needs to be
        tested within the table
        :type column_name: str
        :param constraint_function: a predicate that represent the constraint
        which need to be tested.
        :type constraint_function: def
        """
        #Fra rule_columns_predicate
        self.table_name = table_name
        self.column_name = column_name
        self.constraint_function = constraint_function
        self.wrong_elements = ()

        #Fra rule_row_predicate

        # If column_names is just one string, insert it as list with one element
        if isinstance(column_names, str):
            self.column_names = [column_names]
        else:  # Otherwise just make the list as provided.
            self.column_names = column_names
        self.constraint_function = constraint_function
        self.return_list = return_list
        self.wrong_rows = []

    def run(self, dw_rep):
        """
        Provides each element of the specified column to the given
        constraint function.
        Then logs which elements the constraint function returned
        false on if any.
        """
        if self.column_name and self.column_names:
            raise ValueError("""column_name and column_names must not be
                                assigned at the same time""")
        elif self.column_name:
            self.column(dw_rep)
        elif self.column_names:
            self.row(dw_rep)
        self.report()

    def column(self, dw_rep):
        self.__result__ = True
        for row in dw_rep.get_data_representation(self.table_name):
            # returns the elements at the specified column from each row
            element = row.get(self.column_name.upper())
            # the given constraint function are given the elements here
            if not self.constraint_function(element):
                self.wrong_elements += element,
                self.__result__ = False

    def row(self, dw_rep):
        if inspect.getargspec(self.constraint_function).varargs:  # True
            raise ValueError('Constraints using varargs is not yet supported')

        self.__result__ = True
        if self.return_list:  # True
            for row in dw_rep.get_data_representation(self.table_name):
                # print(row)
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name.upper()))
                # print(element)
                if not self.constraint_function(element):  # False
                    self.wrong_rows.append(row)
            if self.wrong_rows:
                self.__result__ = False
        elif not self.return_list:  # False
            if len(inspect.getargspec(self.constraint_function).args) \
                    != len(self.column_names):
                # print('TESTCODE - Input NOT Acceptable')
                raise ValueError("""Number of columns and number of arguments
                 do not match""")
            for row in dw_rep.get_data_representation(self.table_name):
                # print(row)
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name.upper()))
                # print(element)
                if not self.constraint_function(*element):  # False
                    self.wrong_rows.append(row)
            if self.wrong_rows:
                self.__result__ = False
        else:
            raise TypeError('return_list must be type bool')

    def report(self):
        """
        Reports results of tests. If results return false, it also report which
        elements the constraint function
        returned false upon and in which column these elements belong too.
        """
        if self.column_name and self.column_names:
            raise Exception('column_name and column_names must not be assigned at the same time')
        elif self.column_name:
            return Report(self.__class__.__name__,
                          self.__result__,
                          ': All is well',
                          ': All is not well',
                          self.wrong_elements)
        elif self.column_names:
            return Report(self.__class__.__name__,
                          self.__result__,
                          ': All is well',
                          'at rows {}'.format(self.wrong_rows)
                          )
