__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
import sqlite3
import pygrametl
from pygrametl.datasources import *
from csv import DictReader


class TPredicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def dictify(self, conns):
        """ Creates an iterable of dicts from our connection
        :param  conns: a connection object to a database, which we fetch data from."""
        bicdic = {}
        # Runs over all data source objects
        for table_name, content in conns.items():
            if not isinstance(content, DictReader):
                # Creates a temporary SQLSource object, as we cannot iterate over the same cursor twice.
                temp = SQLSource(connection=content.connection, query=content.query,
                                 names=content.names, parameters=content.parameters)
            else:
                temp = content

            data = []
            # Runs over all entries resulting from the cursor
            for row in temp:
                data.append(row)
            bicdic[table_name] = data

        return bicdic

    def run(self, *args):
        """ Runs the actual test. Stores result in __result__"""
        self.__result__ = True

    def report(self):
        """
        returns the result of the test
        """
        return self.__result__

    def __init__(self, conns):
        """
        :param conns: a dictionary of object connections to the data we need to test.
        """
        tables = self.dictify(conns)
        self.run()
        print(self.report())