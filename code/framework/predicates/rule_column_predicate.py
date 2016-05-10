import inspect
from .predicate import Predicate
from .report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class RuleColumnPredicate(Predicate):
    def __init__(self, table_name, constraint_function, column_names=None,
                 column_names_exclude=False, constraint_input_list=True):

        self.table_name = table_name
        self.constraint_function = constraint_function
        self.column_names = column_names
        self.column_names_exclude = column_names_exclude
        self.constraint_input_list = constraint_input_list
        self.columns = []

    def run(self, dw_rep):

        self.columns = []
        self.column_names = self.setup_columns(dw_rep, self.table_name,
                                               self.column_names,
                                               self.column_names_exclude)
        self.__result__ = True

        function_arguments = inspect.getargspec(self.constraint_function).args
        if len(function_arguments) != len(self.column_names):
            raise ValueError('Number of columns specified and number of' +
                             ' arguments do not match')

        # Collects all column values in lists and places them in a list of lists
        constraint_list = []
        for column_name in self.column_names:
            elements_list = []
            for row in dw_rep.get_data_representation(self.table_name):
                elements_list.append(row.get(column_name.lower()))
            constraint_list.append(elements_list)

        # If constraints should be given as a list, we run our constraints here
        if self.constraint_input_list:
            if not self.constraint_function(*constraint_list):
                self.__result__ = False

        # For each column we create a sum/join, then use that as an argument.
        elif not self.constraint_input_list:
            temp_list = []
            for column in constraint_list:
                if all((isinstance(item, int) or
                            isinstance(item, float) or
                            isinstance(item, complex)) for item in column):
                    temp_list.append(sum(column))
                elif all(isinstance(item, str) for item in column):
                    temp_list.append(''.join(column))
                else:
                    raise TypeError('All elements in column(s) provided is '
                                    'not integers or strings')
            constraint_arg = temp_list

            if len(constraint_arg) == len(self.column_names):
                if not self.constraint_function(*constraint_arg):
                    self.__result__ = False
            else:
                if not self.constraint_function(constraint_arg):
                    self.__result__ = False

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=None,
                      msg='The predicate did not hold against the constraint')
