import inspect
from .predicate import Predicate
from .report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class TablePredicate(Predicate):
    def __init__(self, table_name, constraint_function, column_names=None,
                 column_names_exclude=False, return_list=True):

        self.table_name = table_name
        self.constraint_function = constraint_function
        self.column_names = column_names
        self.column_names_exclude = column_names_exclude
        self.return_list = return_list
        self.columns = []

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

        self.columns = []
        self.setup_columns(dw_rep)
        self.__result__ = True

        if len(inspect.getargspec(self.constraint_function).args) \
                != len(self.column_names):
            raise ValueError('Number of columns specified and number of' +
            ' arguments do not match')

        constraint_list = []
        for column_name in self.column_names:
            elements_list = []
            for row in dw_rep.get_data_representation(self.table_name):
                elements_list.append(row.get(column_name.lower()))
            constraint_list.append(elements_list)

        if self.return_list:
            if not self.constraint_function(*constraint_list):
                self.__result__ = False

        elif not self.return_list:
            temp_list = []
            for column in constraint_list:
                if all(isinstance(item, int) for item in column):
                    temp_list.append(sum(column))
                elif all(isinstance(item, str) for item in column):
                    temp_list.append(''.join(column))
                else:
                    raise TypeError("""All elements in column(s) provided is"""
                     + """ not integers or strings""")
            constraint_arg = temp_list

            if len(constraint_arg) == len(self.column_names):
                if not self.constraint_function(*constraint_arg):
                    self.__result__ = False
            else:
                if not self.constraint_function(constraint_arg):
                    self.__result__ = False

        return Report(self.__result__,
                      self.__class__.__name__,
                      None,
                      'TabelPredicate: FAILED\n'
                      'The predicate did not hold against the constraint')
