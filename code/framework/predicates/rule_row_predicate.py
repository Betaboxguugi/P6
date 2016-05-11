from .predicate import Predicate
from .report import Report
import inspect

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Alexander Brandborg'


class RuleRowPredicate(Predicate):
    """
    Predicate for asserting using a user defined-function returning a bool.
    The function is applied to each row.
    """

    def __init__(self, table_name, constraint_function, column_names=None,
                 constrain_args=[], column_names_exclude=False):
        """
        :param table_name: name of table used for test
        :type table_name: str
        :param column_names: list of column names
        :type column_names: list
        :param constraint_function: user-defined function to run on each row.
        Must return a boolean.
        :type constraint_function: function
        :param costraint_args: Additional arguments for the constrain function.
        :type list
        :param column_names_exclude: bool, indicating how column_names is
        used to fetch columns from the table.
        """
        self.table_name = table_name
        self.constraint_function = constraint_function
        self.constrain_args = constrain_args
        self.column_names = column_names
        self.column_names_exclude = column_names_exclude
        self.wrong_rows = []

    def run(self, dw_rep):
        """
        Runs the constraint function on the specified columns of each row.
        Stores rows asserted faulty by the function for reporting.
        """
        table = dw_rep.get_data_representation(self.table_name)

        # Gets the attribute names for columns needed for test
        column_arg_names = self.setup_columns(dw_rep, self.table_name,
                                              self.column_names,
                                              self.column_names_exclude)

        func_args = inspect.getargspec(self.constraint_function).args
        if len(func_args) != len(column_arg_names) + len(self.constrain_args):
            raise ValueError("""Number of columns and number of arguments
                                do not match""")

        # Iterates over each row, calling the constraint function upon it
        for row in table.itercolumns(column_arg_names):

            # Finds parameters. First attributes then additional params.
            arguments = []
            for name in column_arg_names:
                arguments.append(row[name])

            if self.constrain_args:
                arguments.append(*self.constrain_args)

            # Runs function on parameters
            if not self.constraint_function(*arguments):
                self.wrong_rows.append(row)

        if not self.wrong_rows:
            self.__result__ = True

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=self.wrong_rows,
                      msg=None)
