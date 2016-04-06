__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import test_predicates.t_predicate

parent = test_predicates.t_predicate.TPredicate
conn = sqlite3.connect('test.db')


class HasNull(parent):
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
        self.has_null()
        self.report()

    def has_null(self):
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
        if not self.__result__:
            print('False - Found in table "{}", column "{}"'.format(self.table_name, self.column_name))
            # print(self.__result__)
        else:
            print(self.__result__)

