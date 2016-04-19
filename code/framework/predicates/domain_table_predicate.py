__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

from .predicate import Predicate
from .predicate_report import Report
import inspect


class DomainTablePredicate(Predicate):
    def __init__(self, table_name, column_names, constraint_function, return_list = False):
        # TODO: Make predicate able to accept *args from constraint
        # TODO: Rewrite param and type of all arguments
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_names: list of the column which need to tested against the predicates.
        Note their order in the list, as that is the order they will appear in the constraints args.
        :type column_names: list
        :param constraint_function: a predicate that represent the constraint which need to be tested. May have
        multiple args, but no varargs(no yet supported)
        :type constraint_function:
        """
        self.table_name = table_name
        if isinstance(column_names, str):  # If column_names is just one string, insert it as list with one element
            self.column_names = [column_names]
        else:  # Otherwise just make the list as provided.
            self.column_names = column_names
        self.constraint_function = constraint_function
        self.return_list = return_list
        self.wrong_elements = []

    def run(self, dw_rep):
        """
        Provides a list of element of the specified columns to the given constraint function and its args.
        Then logs which list of elements the constraint function returned false on if any.
        """
        if inspect.getargspec(self.constraint_function).varargs:
            raise ValueError('Constraints using varargs is not yet supported')


        self.__result__ = True
        if self.return_list:
            pass
            for row in dw_rep.get_data_representation(self.table_name):
            # print(row)
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name.upper()))
                # print(element)
                if not self.constraint_function(element):  # False
                    self.wrong_elements.append(element)
                else:  # True
                    pass
            if self.wrong_elements:
                self.__result__ = False
        elif not self.return_list:
            if len(inspect.getargspec(self.constraint_function).args) != len(self.column_names):
                # print('TESTCODE - Input NOT Acceptable')
                raise ValueError('Number of columns and number of arguments do not match')
            for row in dw_rep.get_data_representation(self.table_name):
                # print(row)
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name.upper()))
                # print(element)
                if not self.constraint_function(*element):  # False
                    self.wrong_elements.append(element)
                else:  # True
                    pass
            if self.wrong_elements:
                self.__result__ = False
        else:
            raise TypeError('return_list must be type bool')

    def report(self):
        # TODO: Make proper explanation of report
        """

        """
        return Report(self.__class__.__name__,
                      self.__result__,
                      ': All is well',
                      ': All is not well',
                      self.wrong_elements)
