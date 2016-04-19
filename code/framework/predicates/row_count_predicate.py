__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

from .predicate import Predicate
from .predicate_report import Report


class RowCountPredicate(Predicate):

    def __init__(self, table_name, number_of_rows):
        """
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        self.__result__ = False
        self.table_name = table_name
        self.number_of_rows = number_of_rows
        self.table = []

    def run(self, dw_rep):
        """
        :param dw_rep: A DWRepresentation object allowing us to access our
        table by name
        :return:
        """

        # Extracts contents of table into a list[Dict]
        for row in dw_rep.get_data_representation(self.table_name):
            self.table.append(row)

        rows = len(self.table)
        if rows == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False

    def report(self):
        return Report(self.__class__.__name__,
                      self.__result__
                      )
