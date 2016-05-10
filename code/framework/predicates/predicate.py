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

    def setup_columns(self, dw_rep, table_name,
                      column_names, column_names_exclude):
        """
        Produces a list of columns, which we want to iterate over.
        :param: dw_rep: A DWRepresentation
        :param: table_name: A string indicating a DW table
        :param: column_names: A string or list of attribute names
        :param: column_names_exclude: A bool indicating whether
         the column_names is inclusive or exclusive
        :return chosen_columns: columns we want to iterate over
        """

        # If a single column is given as string, we place it in a list.
        if isinstance(column_names, str):
            column_names = [column_names]

        # If no columns are given
        if not column_names:
            chosen_columns = dw_rep.get_data_representation(table_name).all

        # If we want to exclude column names
        elif column_names_exclude:
            chosen_columns = []
            for name in dw_rep.get_data_representation(table_name).all:
                if name not in column_names:
                    chosen_columns.append(name)

        # If we want to include column names
        else:
            chosen_columns = list(column_names)

        return chosen_columns