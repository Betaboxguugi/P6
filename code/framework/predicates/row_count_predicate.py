__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'

from .predicate import Predicate
from .predicate_report import Report


class RowCountPredicate(Predicate):

    def __init__(self, table_name, number_of_rows):
        """
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        self.__result__ = bool
        self.table_name = table_name
        self.number_of_rows = number_of_rows
        self.table = []
        self.row_number = int

    def run(self, dw_rep):
        """
        :param dw_rep: A DWRepresentation object allowing us to access our
        table by name
        :return:
        """
        self.row_number = 0
        self.table = []

        # Extracts contents of table into a list[Dict]
        for row in dw_rep.get_data_representation(self.table_name):
            self.table.append(row)
            self.row_number += 1

        if len(self.table) == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False

        return self.report()

    def report(self):
        return Report(self.__result__,
                      self.__class__.__name__,
                      None,
                      """{}: FAILED\nThe predicate did not hold, tested for {} row(s), actual number of row(s): {}\n""".format(self.__class__.__name__, self.number_of_rows, self.row_number)
                      )
