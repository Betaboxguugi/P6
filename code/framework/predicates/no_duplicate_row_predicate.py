__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'

from .predicate import Predicate
from .predicate_report import Report


class NoDuplicateRowPredicate(Predicate):

    def __init__(self, table_name, column_names=None, column_names_exclude=False,
                 verbose=False):
        """
        :param table_name: name of table to be checked
        :type table_name: str
        :param column_names: Optional parameter. A list of column names.
        Recommended for when you want to check for duplicates without looking
        at primary keys for example.
        :type column_names: List[str]
        :param column_names_exclude: a bool, if set to true, then the predicate
        will look at all columns excluding the one(s) specified in column_names
        :type column_names_exclude: boo
        :param verbose: if this is set to true information from each step in
        NoDuplicateRowPredicate is printed, this is for debugging purposes.
        :type verbose: bool
        """
        self.table_name = table_name
        self.column_names = column_names
        self.duplicates = []
        set(self.duplicates)
        self.verbose = verbose
        self.table = None
        self.columns = None
        self.dw_rep = None
        self.column_names_exclude = column_names_exclude

    def run(self, dw_rep):
        self.dw_rep = dw_rep
        table = []

        self.table = self.dw_rep.get_data_representation(self.table_name)

        for e in self.table:
            table.append(e)

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
            for e in self.dw_rep.get_data_representation(self.table_name).all:
                temp_columns_list.append(e)
            if self.column_names:
                for e in self.column_names:
                    temp_columns_list.remove(e)
            self.columns = temp_columns_list
        else:
            self.columns = self.column_names

        # We check for duplicates with the columns specified
        while len(table) > 1:
            getting_checked_row = table.pop(0)  # this dict(row) is the one we will check
            if self.verbose:    # against all other rows in the table
                print('Start predicate duplicates')
                print("Rows remaining {}".format(len(table)))
            for row in table:
                if self.verbose:
                    print("Checking table against row: {}".format(getting_checked_row))
                    print("Checking table row: {}".format(row))
                flag = False
                for column in self.columns:
                    x = getting_checked_row.get(column)
                    y = row.get(column)
                    if self.verbose:
                        print("Looking at column '{}'".format(column))
                        print("Looking for value {} with key '{}'".format
                              (x, column))
                        print("Found value {}".format(y))
                    if x != y:  # if two values between the rows are not
                                # duplicates, the rows are not duplicates,
                        if self.verbose:  # and we don't care about the rest of
                            #  the values in those rows
                            print('Unique')
                        flag = False
                        break  # exit the for loop, this brings us to the next
                               # row in the outer for loop
                    else:
                        if self.verbose:
                            print('Duplicate value')
                        flag = True
                if flag and getting_checked_row not in self.duplicates:  # duplicates is a set
                    # and we check if we have already noted this duplicate row
                    if self.verbose:
                        print('Duplicate row found')
                    self.duplicates.append(getting_checked_row)
                if flag and row not in self.duplicates:
                    self.duplicates.append(row)
        if len(self.duplicates) < 1:
            self.__result__ = True
        return self.report()

    def report(self):
        return Report(self.__result__,
                      self.__class__.__name__,
                      self.duplicates,
                      'Unknown Failure')
