# IMPORTS
from .predicate import Predicate
from .report import Report
import time
# Comment
__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Alexander Brandborg'


class ColumnNotNullPredicate(Predicate):
    """
    Predicate for asserting that nulls do not exist in the columns of a table
    """

    def __init__(self, table_name, column_names=None,
                 column_names_exclude=False):
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_names: name of the specified column, which needs to be
        tested within the table
        :type column_names: list or str
        """

        if isinstance(table_name,str):
            self.table_name = [table_name]
        else:
            self.table_name = table_name
        self.rows_with_null = []
        self.column_names = column_names
        self.column_names_exclude = column_names_exclude

    def run(self, dw_rep):
        """
        Iterates over the table, storing any row containing nulls.
        :param dw_rep : DWRepresentation object
        """

        # Gets the columns to iterate over
        chosen_columns = self.setup_columns(dw_rep,self.table_name,
                                            self.column_names,
                                            self.column_names_exclude)

        cursor = dw_rep.connection.cursor()

        null_condition_sql = (x + " IS NULL" for x in chosen_columns)

        pred_sql = " SELECT * " + \
                   " FROM " + " NATURAL JOIN ".join(self.table_name) + \
                   " WHERE " + " OR ".join(null_condition_sql)

        print(pred_sql)
        cursor.execute(pred_sql)
        query_result = cursor.fetchall()

        if not query_result:
            self.__result__ = True

        return Report(result=self.__result__,
                      predicate=self,
                      tables=self.table_name,
                      elements=query_result,
                      msg=None)
