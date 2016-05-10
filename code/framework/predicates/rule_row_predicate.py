from .predicate import Predicate
from .report import Report
import inspect

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class RuleRowPredicate(Predicate):
    def __init__(self, table_name, constraint_function, column_names=None,
                 column_names_exclude=False, constraint_input_list=False):
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
        :param constraint_input_list: If true, constraint_function will be given lists as
         input, if false constraint_function will
        be given args as input. Default is False
        :type constraint_input_list: bool
        """
        self.table_name = table_name
        self.column_names = column_names
        self.constraint_function = constraint_function
        self.constraint_input_list = constraint_input_list
        self.wrong_rows = []
        self.column_names_exclude = column_names_exclude

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

        self.column_names = self.setup_columns(dw_rep, self.table_name,
                                               self.column_names,
                                               self.column_names_exclude)

        # if the constraint takes a list as input
        # For each row we rip out the elements and send to the function
        if self.constraint_input_list:
            for row in dw_rep.get_data_representation(self.table_name):
                element = []
                for column_name in self.column_names:
                    element.append(row.get(column_name))
                if not self.constraint_function(element):
                    self.wrong_rows.append(row)
            if self.wrong_rows:
                self.__result__ = False

        # if the constraint take regular arguments as input
        # For each row we rip out the elements and send to the function
        elif not self.constraint_input_list:
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
            raise TypeError('constraint_input_list must be type bool')

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=self.wrong_rows,
                      msg=None)
