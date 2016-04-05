import os
import sqlite3
import arpeggio as apeg


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
    # Fetches the specified column
    list_column = []
    c.execute("SELECT {} FROM {}".format(column_name, table_name))
    for e in c.fetchall():
        list_column.append(next(iter(e)))

    # Instantiates parser
    parser = apeg.ParserPython(peg)

    correct_parse = 0
    incorrect_parse = 0
    parse_trees = []

    # Determines for each column entry, whether it can be parsed.
    for entry in list_column:
        try:
            parse_trees.append(parser.parse(str(entry)))
            correct_parse += 1
            if verbose:
                print("{} fits the grammar".format(entry))
        except apeg.NoMatch as e:
            incorrect_parse += 1
            e = e.__str__().replace(".", "")
            print("SYNTAX ERROR: {} in {} column".format(e, column_name))
    print("{} fields parsed correctly and {} fields parsed incorrectly".format(correct_parse, incorrect_parse) +
          " in {} column".format(column_name))
    return parse_trees


# Ensures a fresh database to work with.
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
                ('CharLes', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Swedden', 19000.00),
                ('Hannibal', 45, 'Amerrica', 65000.00),
                ('Buggy Bug', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)


# PEG to ensure that entry is at least one digit
def id_format(): return apeg.RegExMatch(r'\d+'), apeg.EOF
print(table_column_syntax_check('COMPANY', 'ID', id_format))


# PEG to ensure that entry begins with capital letter proceeded by lower case letters
def name_format(): return apeg.RegExMatch(r'[A-Z][a-z]+'), apeg.EOF
print(table_column_syntax_check('COMPANY', 'NAME', name_format))


# PEG to ensure that entry is within the given set
def address_format(): return apeg.OrderedChoice(["Denmark", "Texas", "Sweden", "America"]), apeg.EOF
print(table_column_syntax_check('COMPANY', 'ADDRESS', address_format))

# PEG tp ensure that entry is a decimal number
def salary_format(): return apeg.RegExMatch(r'\d+\.\d+'), apeg.EOF
print(table_column_syntax_check('COMPANY', 'SALARY', salary_format()))
