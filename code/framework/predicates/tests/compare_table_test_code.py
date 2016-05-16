import sqlite3
import os
from framework.predicates import CompareTablePredicate
from framework.reinterpreter.datawarehouse_representation import \
    DWRepresentation, DimRepresentation
from pygrametl.tables import Dimension
from pygrametl import ConnectionWrapper
import time

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

company_info = [
                ('Anders', 43, 'Denmark', 21000.00),
                ('Charles', 50, 'Texas', 25000.00),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)",
              company_info)


# Making table to test on...
c.execute('''CREATE TABLE BOMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')

company_info = [('Anders', 43, 'Denmark', 21000.00),
                ('Charles', 50, 'Texas', 25000.00),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000),
                ('Buggy', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO BOMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)",
              company_info)


conn.commit()

ConnectionWrapper(conn)

dim = Dimension('COMPANY', 'ID', ['NAME', 'AGE', 'ADDRESS', 'SALARY'], ['NAME'])
dim_rep = DimRepresentation(dim, conn)

dw = DWRepresentation([dim_rep], conn)

expected_list1 = [
    {'NAME': 'Anders', 'AGE': 43, 'SALARY': 21000.0, 'ADDRESS': 'Denmark',
     'ID': 1},
    {'NAME': 'Charles', 'AGE': 50, 'SALARY': 25000.0, 'ADDRESS': 'Texas',
     'ID': 2},
    {'NAME': 'Wolf', 'AGE': 28, 'SALARY': 19000.0, 'ADDRESS': 'Sweden',
     'ID': 3},
    {'NAME': 'Hannibal', 'AGE': 45, 'SALARY': 65000.0, 'ADDRESS': 'America',
     'ID': 4},
    {'NAME': 'Buggy', 'AGE': 67, 'SALARY': 2000.0, 'ADDRESS': 'America',
     'ID': 5}
]

expected_list2 = expected_list1.copy()
expected_list2.__delitem__(0)
start = time.monotonic()

c = conn.cursor()
c.execute("SELECT * FROM bompany")
compare1 = CompareTablePredicate(['company'], ['bompany'], ['ID'], True, False, (), False, True)



print(compare1.run(dw))
end = time.monotonic()
elapsed = end - start
print('{}{}'.format(round(elapsed, 3), 's'))
conn.close()

