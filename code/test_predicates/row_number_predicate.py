from .TestPredicate import TestPredicate
import sqlite3

class RowPredicate(TestPredicate):

    def __init__(self, conns, tables, number_of_rows):
        """"""
        self.conns = conns
        self.tables = tables
        self.number_of_rows = number_of_rows


    def run(self):
        """"""
        self.conns.execute("SELECT * FROM {}".format(self.tables))
        rows = len(self.conns.fetchall())
        if rows == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False

    #def report(self):




