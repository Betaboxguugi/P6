__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'


from .predicate import Predicate
from .predicate_report import Report

class UniqueKeyPredicate(Predicate):
    """
    Class for testing whether a given primary key is unique on a table
    """

    def __init__(self, table_name, column_names):
        """
        :param connection: A PEP249 connection to a database
        :param table_name: Name of table, which we want to test on
        :param column_names: List of attributes names making up the primary key
        """
        self.cursor = None
        self.table_name = table_name
        self.column_names = column_names
        self.results = []
        self.__result__ = True

    def run(self, dw_rep):
        """
        Creates a list of all primary key instances, of which there are duplicates
        """
        # Gets only the primary key of each entry in the table
        self.cursor = dw_rep.connection.cursor()
        print(",".join(self.column_names))
        self.cursor.execute("SELECT {} FROM {}".format(",".join(self.column_names), self.table_name))

        # Finds duplicates in the resulting SQL table
        found = set()
        duplicates = []
        for item in self.cursor.fetchall():
            if item not in found:
                found.add(item)
            else:
                duplicates.append(item)
                self.__result__ = False

        # Makes the resulting duplicate list unique, so that we do not report the same duplicate twice
        unique_data = [list(x) for x in set(tuple(x) for x in duplicates)]

        # Flattens the list of lists and saves it
        for e in unique_data:
            self.results.append(next(iter(e)))

    def report(self):
        """
        Reports if the primary key was unique
        If not we report the key instances, of which there are duplicates
        """
        return Report(self.__class__.__name__,
                      self.__result__,
                      ': All elements in column(s) {} in table \'{}\' are unique'.format(self.column_names,
                                                                                          self.table_name),
                      ': All elements in column(s) {} in table \'{}\' are NOT unique'.format(self.column_names,
                                                                                              self.table_name),
                      self.results
                      )

"""
# Function, takes a SQL table and print a line for each column, stating whether or not it is a primary key
def table_contain_primary_keys(table_name):

    #:param table_name: name of table we work with
    #PRAGMA, is SQL extension specific to SQLite, used to modify the operation of the SQLite
    #library or to query the SQLite library for internal (non-table) data, as is the case here.
    #table_info returns one row for each column in the named table, which contains various information.
    #The important here is the "pk" column provided, which tells if the column in our table is a primary key.

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
table_contain_primary_keys('COMPANY')

UniqueKeyPredicate(conn, 'COMPANY', ['ID', 'NAME'])

UniqueKeyPredicate(conn, 'COMPANY', ['NAME'])

UniqueKeyPredicate(conn, 'COMPANY', ['ADDRESS'])
"""