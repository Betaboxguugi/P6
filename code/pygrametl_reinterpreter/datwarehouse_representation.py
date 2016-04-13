__author__ = 'Mathias Claus Jensen & Alexander Brandborg'
import os
import sqlite3

class DWRepresentation(object):
    """
    Class used to represent an entire DW.
    Allows for access to specific tables simply through their name.
    """

    def __init__(self, dims, fts, connection):
        """
        :param dims: A list of DimensionRepresentation Objects
        :param fts: A lost of FTRepresentation Objects
        :param connection: A PEP 249 connection to a database
        """

        try:
            self.dims = dims
            self.fts = fts
            self.connection = connection

            # Turns all our names to lower case as SQL is case insensitive
            # Also collects a list of names for a later check
            name_list = []
            rep = self.dims + self.fts
            for entry in rep:
                low = entry.name.lower()
                entry.name = low
                name_list.append(low)

            # Makes sure that no two tables have the same name. Else we raise an exception.
            if len(name_list) != len(list(set(name_list))):
                raise ValueError("Table names are not unique")

            # Fills the up our dictionary with tables keyed by their names.
            self.tabledict = {}
            for entry in rep:
                self.tabledict[entry.name] = entry

        finally:
            try:
                pass
            except Exception:
                pass

    def get_data_representation(self, name):
        """
        :param name: Name of the requested table
        :return: A TableRepresentation Object corresponding to the name
        """
        return self.tabledict[name.lower()]


class TableRepresentation(object):
    """
    Super class for representing tables in a DW
    """

    def __iter__(self):
        """
        :return: A generator for iterating over the contents of the table
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.query)
            names = [t[0] for t in cursor.description]

            while True:
                data = cursor.fetchmany(500)
                # Some cursor.description return null if the cursor hasn't fetched.
                # Thus we call it again after fetch if this is the case.
                if not names:
                    names = [t[0] for t in cursor.description]
                if not data:
                    break
                # Checks that the entries have the correct amount of attributes
                if len(names) != len(data[0]):
                    raise ValueError(
                        "Incorrect number of names provided. " +
                        "%d given, %d needed." % (len(names), len(data[0])))
                for row in data:
                    yield dict(zip(names, row))
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def itercolumns(self, column_names):
        """
        Lets us fetch only a subset of columns from the table
        :param column_names: The subset of columns of interest
        :return: A generator for iterating over the contents of the table
        """
        for data in self.__iter__():
            result = {}
            for name in column_names:
                result.update({name: data[name]})
            yield result


class DimRepresentation(TableRepresentation):
    """
    An object for representing data in a DW dimension
    """
    def __init__(self, name, key, attributes, lookupatts, connection, query=None):
        """
        :param name: Name of table
        :param key: Name of primary key attribute
        :param attributes: List of non-lookup attributes of the table
        :param lookupatts: List of lookup attributes of the table
        :param connection: PEP249 connection to a database
        :param query: SQL query used for fetching contents of the table
        """
        self.name = name
        self.key = key
        self.attributes = attributes
        self.lookupatts = lookupatts
        self.connection = connection
        self.all = [self.key] + self.attributes + self.lookupatts

        if query is None:
            self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name
        else:
            self.query = query


class FTRepresentation(TableRepresentation):
    """
    An Object for representing data in a DW fact table
    """
    def __init__(self, name, keyrefs, measures, connection, query=None):
        """
        :param name: Name of table
        :param keyrefs: List of attributes that are foreign keys to other tables
        :param measures: List of attributes containing non-key values
        :param connection: PEP249 connection to a database
        :param query: SQL query used for fetching contents of the table
        """
        self.name = name
        self.keyrefs = keyrefs
        self.measures = measures
        self.connection = connection
        self.all = self.keyrefs + self.measures

        if query is None:
            self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name
        else:
            self.query = query


"""
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
                ('Wolf', 28, 'Sweden', 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy Bug', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

p = conn.cursor()

p.execute('''CREATE TABLE BOMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')

company_info = [('Anders', 43, 'Denmark', 21000.00),
                ('CharLes', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Sweden', 19000.00),
                ('Hannibal', 45, 'America', 65000.00),
                ('Buggy Bug', 67, 'America', 2000)
                ]

# ... and inserting the necessary data.
p.executemany("INSERT INTO BOMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

a = DimRepresentation('COMPANY', 'ID', ['AGE', 'ADDRESS', 'SALARY'], ['NAME'], conn)
b = FTRepresentation('BOMPANY', ['NAME', 'ADDRESS', 'ID'], ['AGE', 'SALARY'], conn)
c = DWRepresentation([a], [b], conn)

print(c.get_data_representation('BOMPANY').name)
for d in c.get_data_representation('BOMPANY').itercolumns(['ID']):
    print(d['ID'])
"""