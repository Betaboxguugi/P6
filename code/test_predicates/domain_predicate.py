__author__ = 'Arash Michael Sami Kjær and Mikael Vind Mikkelsen'
__maintainer__ = 'Arash Michael Sami Kjær and Mikael Vind Mikkelsen'

from test_predicates.t_predicate import TPredicate


class DomainPredicate(TPredicate):
    def __init__(self, conn, table_name, column_name, constraint_function):
        """
        :param conn: a connection object to a database, which we fetch data from.
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_name: name of the specified column, which needs to be tested within the table
        :type column_name: str
        :param constraint_function: a function that represent the constraint which need to be tested. Must return true or false
        :type constraint_function: def
        """

        self.database = self.dictify(conn)
        self.table = self.database.get(table_name)
        self.column_name = column_name
        self.constraint_function = constraint_function
        self.wrong_elements = ()

    def run(self):
        """
        Provides each element of the specified column to the given constraint function.
        Then logs which elements the constraint function returned false on if any, then finally calls report
        """

        self.__result__ = True
        self.wrong_elements = ()
        for row in self.table:
            element = row.get(self.column_name)  # returns the elements at the specified column from each row
            if not self.constraint_function(element):  # the given constraint function are given the elements here
                self.wrong_elements += element,
                self.__result__ = False
        self.report()

    def report(self):
        """
        Reports results of tests. If results return false, it also report which elements the constraint function
        returned false upon and in which column these elements belong too.
        """
        if self.wrong_elements:
            print('In the column "{}", the following elements does now uphold the constraint: {}'.format(
                self.column_name,
                self.wrong_elements))
        print(self.__result__)
