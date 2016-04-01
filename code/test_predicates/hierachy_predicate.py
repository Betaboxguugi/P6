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
        sqlunion = []

        for f in self.func_dependencies:
            alpha = f[0]
            beta = f[1]

            alphasql = set()
            for a in alpha:
                alphasql.add(" A." + a + "=B." + a + " ")

            s = " AND "
            where_alpha = s.join(alphasql)

            t = " OR "
            betasql = set()
            for b in beta:
                betasql.add(" A." + b + "<>B." + b + " ")

            where_beta = t.join(betasql)

            fsql = "SELECT *,  AS funcd FROM " + self.name + " AS A, " + self.name + " AS B " \
                  "WHERE" + where_alpha + " AND (" + where_beta + ")"

            sqlunion.append(fsql)


        func_dep_sql = " UNION ".join(sqlunion)

        self.cursor.execute(func_dep_sql)
        result = self.cursor.fetchall()
        print(result)
        if not result:
            self.results.append(True)
        else:
            self.results.append(False)

    def report(self):
        for res in self.results:
            print(res)

    def __init__(self, connection, tables, func_dependencies):

        self.connection = connection
        self.func_dependencies = func_dependencies
        self.results = []
        self.cursor = self.connection.cursor()

        if len(tables) == 1:
            tablesql = "SELECT * FROM " + tables[0] + " AS JIM"
            print(tablesql)

        else:
            tablesql = "SELECT * FROM " + " NATURAL JOIN".join(tables)

        self.cursor.execute(tablesql)

        self.run()
        self.report()


DW_NAME = './sales.db'

dw_conn = sqlite3.connect(DW_NAME)

tables = ['sales']
funcd = [(['saleid', 'book'], ['genre']), (['city'], ['book'])]

a = HierachyPredicate(dw_conn, tables, funcd)
