import os
import sqlite3
from test_predicates.duplicate_rows_predicate import DuplicatePredicate
from pygrametl.datasources import SQLSource

# This just insures we have a fresh database to work with.
if os.path.isfile('test.db'):
    os.remove('test.db')
    print("Deleted previous database")
    conn = sqlite3.connect('test.db')
else:
    conn = sqlite3.connect('test.db')

c = conn.cursor()
print("Opened database successfully")

# Making table to test on...
c.execute('''CREATE TABLE COMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')
print("Table created successfully")

company_info = [('Anders', 43, 'Denmark', 21000.00),
                ('Charles', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Sweden', 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)
print('Data inserted into table')
dic = dict()
dic['company'] = SQLSource(connection=conn, query="SELECT * FROM company")
columns = ('name', 'age', 'address', 'salary')
columns_cap = ('NAME', 'AGE', 'ADDRESS', 'SALARY')
dup_predicate = DuplicatePredicate(dic, 'company', columns)
dup_predicate.run()

