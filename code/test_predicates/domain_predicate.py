from test_predicates.t_predicate import TPredicate

class DomainPredicate (TPredicate):

    def __init__(self, conn, table_name, column_name, constraint_function):
        # TODO: Make a proper explanation of inputs
        """
        :param conn: a SQL connection object, which we fetch data from.
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
        self.wrong_values = ()

    def run(self):
        self.__result__ = True
        self.wrong_values = ()
        for row in self.table:
            value = row.get(self.column_name)
            if not self.constraint_function(value):
                self.wrong_values += value,
                self.__result__ = False
        self.report()

    def report(self):
        if self.wrong_values:
            print(self.wrong_values)
        print(self.__result__)
