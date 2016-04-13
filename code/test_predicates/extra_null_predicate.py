__co-author__ = 'Alexander Brandborg'

"""Function which test if all keys in a table is unique and the functions necessary to achieve this"""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import os, sys
import os.path


def has_null(table_name, column_name):
    c.execute("SELECT {} FROM {}".format(column_name, table_name))
    cc = c.fetchall()
    column_length = len(cc)
    for x in range(0, column_length):
        if cc[x][0] is None:
            print("NULL DETECTED ABANDON SHIP!")
            break
        else:
            print("All is well")


def smarter_has_null(table_name, column_name):
    c.execute("SELECT {} FROM {} ORDER BY {}".format(column_name, table_name, column_name))
    cc = c.fetchall()
    column_length = len(cc)
    if cc[0][0] is None:
        print("NULL DETECTED ABANDON SHIP!!")
    elif cc[column_length-1][0] is None:
        print("NULL DETECTED ABANDON SHIP!!!")
    else:
        print('All is well')

# This just insures we have a fresh database to work with.
TEST_DB = 'test.db'
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

conn = sqlite3.connect(TEST_DB)
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
                ('Wolf', 28, None, 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy', 67, 'America', 2000),
                ('Bombay', 34, 'Sweden', 35000.00)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)


# IGNORE, experimental area for various smaller things.
print('WAT ---------------------------------------------------------------------------------------')
c.execute("SELECT ADDRESS FROM '%s'" % 'COMPANY')
print(c.fetchall())

c.execute("PRAGMA table_info(COMPANY)")
print(c.fetchall())

c.execute("PRAGMA table_info(COMPANY)")
print(len(c.fetchall()))

c.execute("PRAGMA table_info(COMPANY)")
print(c.fetchall()[0][5])
print('NONWAT ------------------------------------------------------------------------------------')

# Examples of how to use the functions as they are now

has_null('COMPANY', 'ADDRESS')

smarter_has_null('COMPANY', 'ADDRESS')