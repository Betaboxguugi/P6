__author__ = 'Alexander'
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
from framework.reinterpreter.datawarehouse_representation import *
import  sqlite3
import os

path = "C:/Users/Alexander/Documents/GitHub/P6/code/framework/reinterpreter/sample_program.py"

n = ColumnNotNullPredicate('Company', 'Name')
m = CompareTablePredicate('Company','Bompany')

input_conn = sqlite3.connect('input.db')
output_conn = sqlite3.connect('output.db')


if os.path.exists('dw.db'):
    os.remove('dw.db')

dw_conn = sqlite3.connect('dw.db')

sales_cur = dw_conn.cursor()

# We make a new table
sales_cur.execute("CREATE TABLE dim1 " +
                    "(key1 INTEGER PRIMARY KEY, attr1 INTEGER, attr2 INTEGER)")

sales_cur.execute("CREATE TABLE dim2 " +
                    "(key2 INTEGER PRIMARY KEY, attr3 INTEGER, attr4 INTEGER)")

sales_cur.execute("CREATE TABLE ft1 " +
                    "(key1 INTEGER PRIMARY KEY)")



Case(path, {'a': input_conn, 'b': output_conn, 'c': dw_conn}, [n], True)
