from code.test_predicates.t_predicate import TPredicate


class RowPredicate(TPredicate):

    def __init__(self, conn):
        """"""
        self.__result__ = False
        self.table = self.dictify(conn)
        self.table_name = ''
        self.number_of_rows = None


    def run(self, table_name, number_of_rows):
        """
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        self.table_name = table_name
        self.number_of_rows = number_of_rows
        rows = len(self.table[self.table_name])
        if rows == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False
