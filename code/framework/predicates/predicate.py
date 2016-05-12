__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from pygrametl.datasources import *
from csv import DictReader


class Predicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def run(self, *args):
        """ Runs the actual test. Stores result in __result__"""
        self.__result__ = True

    def setup_columns(self, dw_rep, table_names,
                      column_names=None, column_names_exclude=False):
        """
        Produces a list of columns, which we want to iterate over.
        :param: dw_rep: A DWRepresentation
        :param: table_names: A string indicating a DW table
        :param: column_names: A string or list of attribute names
        :param: column_names_exclude: A bool indicating whether
         the column_names is inclusive or exclusive
        :return chosen_columns: columns we want to iterate over
        """


        # If a single column is given as string, we place it in a list.
        if isinstance(column_names, str):
            column_names = [column_names]
        # Same again with table_names
        if isinstance(table_names, str):
            table_names = [table_names]

        chosen_columns = set()
        table_names = set(table_names)
        if column_names:
            column_names = set(column_names)
        else:
            column_names = set()

        # If no columns are given we add all columns
        if not column_names:
            for table in table_names:
                chosen_columns.update(dw_rep.get_data_representation(table).all)

        # If we want to exclude column names
        elif column_names_exclude:
            for table in table_names:
                chosen_columns.update(set(dw_rep.get_data_representation(table).all) - column_names)

        # If we want to include column names
        else:
            chosen_columns = column_names

        return chosen_columns
