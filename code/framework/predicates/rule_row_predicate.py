from .predicate import Predicate
from .predicate_report import Report
import inspect

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class RuleRowPredicate(Predicate):
    def __init__(self, table_name, constraint_function, column_names=None,
                 column_names_exclude=False, return_list=False):
        # TODO: Make predicate able to accept *args from constraint
        """
        :param table_name: name of table where the test will be run
        :type table_name: str
        :param column_names: list of all the columns which need to tested
        against the predicates.
        Note their order in the list, as that is the order they will appear in
        the constraints args.
        :type column_names: list
        :param constraint_function: a predicate that represent the constraint
        which need to be tested. May take
        multiple args or a list, but no varargs(not yet supported). Must return
         true or false for each row given.
        :type constraint_function: function
        :param return_list: If true, constraint_function will be given lists as
         input, if false constraint_function will
        be given args as input. Default is False
        :type return_list: bool
        """
        self.table_name = table_name

        self.column_names = column_names
        self.constraint_function = constraint_function
        self.return_list = return_list
        self.wrong_rows = []
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
            for column in dw_rep.get_data_representation(
                    self.table_name).all:
                temp_columns_list.append(column)
            if self.column_names:
                for column_name in self.column_names:
                    temp_columns_list.remove(column_name)
            self.column_names = temp_columns_list

    def run(self, dw_rep):
        """
        Provides a list of element of the specified columns to the given
         constraint function and its args.
        Then logs which list of elements the constraint function returned
         false on if any.
        """
        if inspect.getargspec(self.constraint_function).varargs:  # True
            raise ValueError('Constraints using varargs is not yet supported')

        self.__result__ = True

        self.setup_columns(dw_rep)

        if self.return_list:
            for row in dw_rep.get_data_representation(self.table_name):
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name))
                if not self.constraint_function(element):
                    self.wrong_rows.append(row)
            if self.wrong_rows:
                self.__result__ = False
        elif not self.return_list:
            if len(inspect.getargspec(self.constraint_function).args)\
                   != len(self.column_names):
                raise ValueError("""Number of columns and number of arguments
                 do not match""")
            for row in dw_rep.get_data_representation(self.table_name):
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name))
                if not self.constraint_function(*element):
                    self.wrong_rows.append(row)
            if self.wrong_rows:
                self.__result__ = False
        else:
            raise TypeError('return_list must be type bool')
        return self.report()

    def report(self):
        return Report(self.__result__,
                      self.__class__.__name__,
                      self.wrong_rows,
                      'Unknown Error'
                      )
