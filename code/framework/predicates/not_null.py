__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
from ..predicates.predicate import Predicate
from ..predicate_report import Report

conn = sqlite3.connect('test.db')

class NotNull(Predicate):
    def __init__(self, table_name, column_name):
        """
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_name: name of the specified column, which needs to be tested within the table
        :type column_name: str
        """
        self.table_name = table_name
        self.column_name = column_name

    def run(self, dw_rep):
        """
        Then checks each element in the specified column,
        if any are null, it sets self.__result__ to false. Finally calls self.report()
        """
        self.__result__ = True
        for row in dw_rep.get_data_representation(self.table_name):
            if row.get(self.column_name) is None:
                self.__result__ = False
                break
        self.report()


    def report(self):
        """
        If null is found, prints what table and column null resides in, otherwise prints true
        """
        return Report(self.__class__.__name__,
                      self.__result__
                      )

