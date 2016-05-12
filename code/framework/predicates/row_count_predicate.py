__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'

from .predicate import Predicate
from .report import Report


class RowCountPredicate(Predicate):

    def __init__(self, table_name, number_of_rows):
        """
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        if isinstance(table_name, str):
            self.table_name = list(table_name)
        else:
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

        pred_sql = \
            " SELECT COUNT(*) " + \
            " NATURAL JOIN ".join(self.table_name)

        cursor = dw_rep.connection.cursor()
        cursor.execute(pred_sql)
        query_result = cursor.fetchall()

        if query_result == self.number_of_rows:
            self.__result__ = True


        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=None,
                      msg="""The predicate did not hold, tested for {} row(s),
                      actual number of row(s): {}""".format(
                          self.number_of_rows, query_result
                      ))


