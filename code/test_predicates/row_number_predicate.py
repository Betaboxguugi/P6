from test_predicates.t_predicate import TPredicate

class RowPredicate(TPredicate):

    def __init__(self, conn, table_name, number_of_rows):
        """
        :param conn: a dictionary of SQLSource objects
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        self.__result__ = False
        self.table = self.dictify(conn)
        self.table_name = table_name
        self.number_of_rows = number_of_rows

    def run(self):
        rows = len(self.table[self.table_name])
        if rows == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False
        self.report()

    def report(self):
        print(self.__result__)

