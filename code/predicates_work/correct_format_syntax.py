import os
import sqlite3
import arpeggio as apeg

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
                ('CharlDes', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Swedden', 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy', 67, 'Amerrica', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)
print('Data inserted into table')


def table_column_syntax_check(table_name, column_name, peg, verbose=False):
    """
    Takes a table, a column and a Parsing Expression Grammar as defined in the arpeggio Python package.
    It then attempts to parse it following the rules of the grammar.
    """
    c.execute("SELECT {} FROM {}".format(column_name, table_name))
    column_length = len(c.fetchall())
    list_column = []
    for x in range(0, column_length):
        c.execute("SELECT {} FROM {}".format(column_name, table_name))
        list_column.insert(0, c.fetchall()[x][0])
    # print(list_column)
    parser = apeg.ParserPython(peg)
    for entry in list_column:
        try:
            parser.parse(str(entry))
            if verbose:
                print(str(entry) + " fits the grammar")
        except apeg.NoMatch as e:
            e = e.__str__().replace(".", "")
            print("SYNTAX ERROR: " + e + " in " + column_name + " column")








"""PEG Stuff"""
# PEG Parsing Expression Grammar


def id_format(): return apeg.RegExMatch(r'\d+'), apeg.EOF


def name_format(): return apeg.RegExMatch(r'[A-Z][a-z]+'), apeg.EOF


def address_format(): return apeg.OrderedChoice(["Denmark", "Texas", "Sweden", "America"]), apeg.EOF

"""Not PEG stuff"""

table_column_syntax_check('COMPANY', 'ID', id_format, verbose=True)
table_column_syntax_check('COMPANY', 'NAME', name_format, verbose=True)
table_column_syntax_check('COMPANY', 'ADDRESS', address_format, verbose=True)
