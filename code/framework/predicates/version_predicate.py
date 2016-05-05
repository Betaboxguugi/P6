from .predicate import Predicate
from .report import Report

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


class VersionPredicate(Predicate):
    def __init__(self, table_name):
        self.table_name = table_name

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
        pass

    def run(self, dw_rep):

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=None,
                      msg=None)
