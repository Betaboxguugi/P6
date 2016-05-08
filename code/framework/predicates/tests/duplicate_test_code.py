import sqlite3
import os
from framework.predicates import NoDuplicateRowPredicate as DuplicatePredicate
from framework.reinterpreter.datawarehouse_representation import \
    DWRepresentation, DimRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

# This just ensures we have a fresh database to work with.
open(os.path.expanduser('test.db'), 'w')

conn = sqlite3.connect('test.db')

c = conn.cursor()

# Making table to test on...
c.execute('''CREATE TABLE COMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')

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
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)",
              company_info)
conn.commit()
columns = ['NAME', 'AGE', 'ADDRESS', 'SALARY']

dim = DimRepresentation('COMPANY', 'ID', ['NAME', 'AGE', 'ADDRESS', 'SALARY'],
                        conn, ['NAME'])
dw = DWRepresentation([dim], conn)

dup_predicate = DuplicatePredicate('company', ['ID'], True)
print(dup_predicate.run(dw))

conn.close()
