__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
import sqlite3
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource

class TPredicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def dictify(self, conns):
        """ Creates an iterable of dicts from our connection
        :param  conn: a pygrametl connection object, which we wish to fetch data from"""
        bicdic = {}
        for table_name, content in conns.items():
            data = []
            for row in content:
               data.append(row)
            bicdic[table_name] = data
        return bicdic

    def run(self):
        """ Runs the actual test. Stores result in __result__"""
        self.__result__ = True

    def report(self):
        """
        returns the result of the test
        """
        return self.__result__

    def __init__(self, conns):
        """
        :param conns: a tuple of object connections to the data we need to test.
        """
        tables = self.dictify(conns)
        print(tables['sales'])
        print(tables['region'])
        print(self.report())
        self.run()
        print(self.report())

"""
SALES_DB_NAME = './sales.db'
CSV_NAME = './region.csv'
sales_conn = sqlite3.connect(SALES_DB_NAME)
csv_file_handle = open(CSV_NAME, "r")

dic = {}
dic['sales'] = SQLSource(connection=sales_conn, query="SELECT * FROM sales")
dic['region'] = CSVSource(f=csv_file_handle, delimiter=',')
TPredicate(dic)"""