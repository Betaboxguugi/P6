from t_predicate import TPredicate

class RowPredicate(TPredicate):

    def __init__(self, dw_rep, table_name, number_of_rows):
        """
        :param dw_rep: A DWRepresentation object allowing us to access our table by name
        :param table_name: name of the table we are testing
        :param number_of_rows: number of rows we are testing for
        """
        self.__result__ = False

        # Extracts contents of table into a list[Dict]
        self.table = []
        for row in dw_rep.get_data_representation(table_name):
            self.table.append(row)

        self.table_name = table_name
        self.number_of_rows = number_of_rows

    def run(self):
        rows = len(self.table)
        if rows == self.number_of_rows:
            self.__result__ = True
        else:
            self.__result__ = False

    def report(self):
        print(self.__result__)

