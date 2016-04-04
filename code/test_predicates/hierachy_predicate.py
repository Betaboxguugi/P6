__author__ = 'Alexander'

import sqlite3
import pygrametl
from pygrametl.datasources import *
from csv import DictReader
from t_predicate import TPredicate
import itertools
from functools import reduce

class HierachyPredicate(TPredicate):
    def run(self):
        for f in self.func_dependencies:
            alpha = str(f[0])
            beta = str(f[1])

            sql = "SELECT * FROM " + self.name + " AS A, " + self.name + " AS B " \
                "WHERE A." + alpha + "=B." + alpha + \
                " AND A." + beta + "<>B." + beta

            print(sql)

            cursor = source.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if(not result):
                self.results.append(True)
            else:
                self.results.append(False)

        #SELECT * from R AS r1, R AS r2 WHERE r1.A=r2.A AND r1.B <> r2.B


    def report(self):
        for res in self.results:
            print(res)

    def __init__(self, name, table, func_dependencies):

        self.name = name
        self.table = table
        self.connection = table.connection
        self.func_dependencies = func_dependencies
        self.results = []

        self.run()
        self.report()


SALES_DB_NAME = './sales.db'

sales_conn = sqlite3.connect(SALES_DB_NAME)
source = SQLSource(connection=sales_conn, query="SELECT * FROM sales")

l = [('saleid','book'),('city','book')]

a =  HierachyPredicate('sales', source, l)

