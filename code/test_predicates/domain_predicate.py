__author__ = 'Arash Michael Sami Kjær and Mikael Vind Mikkelsen'
__maintainer__ = 'Arash Michael Sami Kjær and Mikael Vind Mikkelsen'

from t_predicate import TPredicate


class DomainPredicate(TPredicate):
    def __init__(self, dw_rep, table_name,  column_name, constraint_function,):
        """
        :param dw_rep: a DWRepresentation letting us access tables through names
        :type  DWRepresentation
        :param table_name: name of specified table which needs to be tested
        :type table_name: str
        :param column_name: name of the specified column, which needs to be tested within the table
        :type column_name: str
        :param constraint_function: a predicate that represent the constraint which need to be tested.
        :type constraint_function: def
        """

        # Gets table entries from the specified column and stores them in a list
        self.table = []
        for row in dw_rep.get_data_representation(table_name).itercolumns([column_name]):
            self.table.append(row[column_name])

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
            if not self.constraint_function(row):  # the given constraint function are given the elements here
                self.wrong_elements += row,
                self.__result__ = False
        self.report()

    def report(self):
        """
        Reports results of tests. If results return false, it also report which elements the constraint function
        returned false upon and in which column these elements belong too.
        """
        if self.wrong_elements:
            print('In the column "{}", the following elements does not uphold the constraint: {}'.format(
                self.column_name,
                self.wrong_elements))
        print(self.__result__)
