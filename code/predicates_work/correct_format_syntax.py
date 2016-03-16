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
                ('CharLes', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Swedden', 19000.00),
                ('Hannibal', 45, 'Amerrica', 65000.00),
                ('Buggy Bug', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)
print('Data inserted into table')


def table_column_syntax_check(table_name, column_name, peg, verbose=False):
    """
    Takes a table, a column and a Parsing Expression Grammar as defined in the arpeggio Python package.
    It does not need the entire grammar as parameter, only the root rule that points to the other definitions.
    example:

    def root_rule(): return other_rule, EOF
    def other_rule(): return arpeggio.RegExMatch('Hello '), another_rule
    def another_rule(): return arpeggio.RegExMatch('World!')

    you would give root_rule as the peg parameter

    It then generates a parser and tries to parse the fields in the column.
    """
    c.execute("SELECT {} FROM {}".format(column_name, table_name))
    column_length = len(c.fetchall())
    list_column = []
    for x in range(0, column_length):
        c.execute("SELECT {} FROM {}".format(column_name, table_name))
        list_column.insert(0, c.fetchall()[x][0])
    # print(list_column)
    parser = apeg.ParserPython(peg)
    correct_parse = 0
    incorrect_parse = 0
    for entry in list_column:
        # print(entry)
        try:
            parser.parse(str(entry))
            correct_parse += 1
            if verbose:
                print(str(entry) + " fits the grammar")
        except apeg.NoMatch as e:
            incorrect_parse += 1
            e = e.__str__().replace(".", "")
            print("SYNTAX ERROR: " + e + " in " + column_name + " column")
    print(str(correct_parse) + " fields parsed correctly " + str(incorrect_parse) + " fields parsed incorrectly")








"""PEG Stuff"""
# PEG Parsing Expression Grammar


def id_format(): return apeg.RegExMatch(r'\d+'), apeg.EOF


def name_format(): return apeg.RegExMatch(r'[A-Z][a-z]+'), apeg.EOF


def address_format(): return apeg.OrderedChoice(["Denmark", "Texas", "Sweden", "America"]), apeg.EOF


def salary_format(): return apeg.RegExMatch(r'\d+\.\d+'), apeg.EOF


"""Not PEG stuff"""

table_column_syntax_check('COMPANY', 'ID', id_format)
table_column_syntax_check('COMPANY', 'NAME', name_format)
table_column_syntax_check('COMPANY', 'ADDRESS', address_format)
table_column_syntax_check('COMPANY', 'SALARY', salary_format())

