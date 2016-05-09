from .predicate import Predicate
from .report import Report

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class NoDuplicateRowPredicate(Predicate):

    def __init__(self, table_name, column_names=None,
                 column_names_exclude=False):
        """
        :param table_name: name of table to be checked
        :type table_name: str
        :param column_names: Optional parameter. A list of column names.
        Recommended for when you want to check for duplicates without looking
        at primary keys for example.
        :type column_names: List[str]
        :param column_names_exclude: a bool, if set to true, then the predicate
        will look at all columns excluding the one(s) specified in column_names
        :type column_names_exclude: bool"""

        self.table_name = table_name
        self.column_names = column_names
        self.duplicates = []
        self.table = None
        self.columns = None
        self.column_names_exclude = column_names_exclude

    def run(self, dw_rep):
        self.setup_columns(dw_rep)
        hts = {}
        self.table = dw_rep.get_data_representation(self.table_name)
        for row in self.table.itercolumns(self.columns):
            row_tuple = tuple(row.values())
            if row_tuple not in hts:
                hts[row_tuple] = True
            else:
                self.duplicates.append(row)

        return self.report()

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
            for e in dw_rep.get_data_representation(self.table_name).all:
                temp_columns_list.append(e)
            if self.column_names:
                for e in self.column_names:
                    temp_columns_list.remove(e)
            self.columns = temp_columns_list
        else:
            self.columns = self.column_names

    def report(self):

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=self.duplicates,
                      msg=None)

