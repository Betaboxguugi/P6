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
        Creates a list of all primary key instances,
        of which there are duplicates
        """
        # Gets only the primary key of each entry in the table
        self.cursor = dw_rep.connection.cursor()
        print(",".join(self.column_names))
        self.cursor.execute("SELECT {} FROM {}".format(
            ",".join(self.column_names), self.table_name))

        # Finds duplicates in the resulting SQL table
        found = set()
        duplicates = []
        for item in self.cursor.fetchall():
            if item not in found:
                found.add(item)
            else:
                duplicates.append(item)
                self.__result__ = False

        # Makes the resulting duplicate list unique,
        # so that we do not report the same duplicate twice
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
                      """: All elements in column(s) {} in table \'{}\'
                      are unique""".format(self.column_names,
                                           self.table_name),
                      """: All elements in column(s) {} in table \'{}\'
                      are NOT unique""".format(self.column_names,
                                               self.table_name),
                      self.results
                      )

