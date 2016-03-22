"""Function which test if all keys in a table is unique and the functions necessary to achieve this"""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import os, sys
import os.path

# IGNORE, an old attempt that failed but still around if i wish to actually do it
class Table:
    """Optional Documentation string"""

    def __init__(self, table_name):
        self.table_name = table_name

    def print_table(self):
        """Prints the given table"""
        c.execute("SELECT * FROM '%s'" % self.table_name)
        # c.execute("SELECT * FROM ?", self.table_name)
        print(c.fetchall())


# Function, takes a SQL table and print a line for each column, stating whether or not it is a primary key
def table_contain_primary_keys(table_name):
    # PRAGMA, is SQL extension specific to SQLite, used to modify the operation of the SQLite
    # library or to query the SQLite library for internal (non-table) data, as is the case here.
    # table_info returns one row for each column in the named table, which contains various information. The
    # important here is the "pk" column provided, which tells if the column in our table is a primary key.
    c.execute("PRAGMA table_info('%s')" % table_name)
    number_of_columns = len(c.fetchall())
    for x in range(0, number_of_columns):
        c.execute("PRAGMA table_info('%s')" % table_name)
        if c.fetchall()[x][5] == 1:
            c.execute("PRAGMA table_info('%s')" % table_name)
            print(c.fetchall()[x][1] + ' is a primary key')
        else:
            c.execute("PRAGMA table_info('%s')" % table_name)
            print(c.fetchall()[x][1] + ' is NOT a primary key')


# Function, returns true if it finds any duplicates in a list or false if none are found.
# Used in function table_column_contain_unique_keys
def any_dup(the_list):
    seen = set()
    for x in the_list:
        if x in seen:
            return True
        seen.add(x)
    return False


# Function, takes a SQL table and name of a column in it, then prints a line,
# stating whether all entries in that column are unique
def table_column_contain_unique_keys(table_name, column_name):
    c.execute("SELECT {} FROM {}".format(column_name, table_name))
    column_length = len(c.fetchall())
    list_column = []
    for x in range(0, column_length):
        c.execute("SELECT {} FROM {}".format(column_name, table_name))
        list_column.append(c.fetchall()[x][0])
    if any_dup(list_column) is True:
        print('All entries in column {} in table {} are NOT unique'.format(column_name, table_name))
    else:
        print('All entries in column {} in table {} are unique'.format(column_name, table_name))


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
                ('Wolf', 28, None, 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy', 67, 'America', 2000),
                ('Bombay', 34, 'Sweden', 35000.00)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)
print('Data inserted into table')

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
table_contain_primary_keys('COMPANY')

table_column_contain_unique_keys('COMPANY', 'ID')

table_column_contain_unique_keys('COMPANY', 'NAME')

table_column_contain_unique_keys('COMPANY', 'ADDRESS')

has_null('COMPANY', 'ADDRESS')

smarter_has_null('COMPANY', 'ADDRESS')