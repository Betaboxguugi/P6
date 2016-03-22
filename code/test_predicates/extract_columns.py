import sqlite3
from pygrametl.datasources import SQLSource, CSVSource
from test_predicates.t_predicate import TPredicate


def extract_columns(dic, table_name, column_name):
    ec_dic = dic
    ec_table_name = table_name
    ec_column_name = column_name
    ec_dic_length = len(ec_dic)
    for x in range(0, ec_dic_length):
        print('Iteration: {}'.format(x))


SALES_DB_NAME = './sales.db'
CSV_NAME = './region.csv'
sales_conn = sqlite3.connect(SALES_DB_NAME)
csv_file_handle = open(CSV_NAME, "r")

dic = {}
dic['sales'] = SQLSource(connection=sales_conn, query="SELECT * FROM sales")
dic['sal2s'] = dic['sales']
dic['region'] = CSVSource(f=csv_file_handle, delimiter=',')

extract_columns(dic, 'sales', 'sale')



TPredicate(dic)