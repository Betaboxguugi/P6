__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import test_predicates.t_predicate
from test_predicates.report import Report


parent = test_predicates.t_predicate.TPredicate
conn = sqlite3.connect('test.db')


class NotNull(parent):
    def __init__(self, conn, table_name, column_name):
        """
        :param conn: a dictionary of SQLSource objects
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_name: name of the specified column, which needs to be tested within the table
        :type column_name: str
        """
        self.database = self.dictify(conn)
        self.table_name = table_name
        self.table = self.database.get(table_name)
        self.column_name = column_name

    def run(self):
        """
        Set self.__result__ to true as we hope everything goes well, then calls self.has_null() which may change
        self.__result__ into False. Finally calls self.report()
        """
        self.__result__ = True
        self.not_null()
        self.report()

    def not_null(self):
        """
        Checks each element in the specified column, if any are null, it sets self.__result__ to false
        """
        for row in self.table:
            if row.get(self.column_name) is None:
                self.__result__ = False
                break

    def report(self):
        """
        If null is found, prints what table and column null resides in, otherwise prints true
        """
        Report(self.__class__.__name__, self.__result__)

