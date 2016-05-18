from .predicate import Predicate
from .report import Report

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg'


class NoDuplicateRowPredicate(Predicate):
    """
    Predicate for asserting whether duplicated rows appear in a table.
    """

    def __init__(self, table_name, column_names=None,
                 column_names_exclude=False):
        """
        :param table_name: name of table to be checked
        :type table_name: str
        :param column_names: A list of column names.
        Recommended for when you want to check for duplicates without looking
        at primary keys for example.
        :type column_names: List[str]
        :param column_names_exclude: a bool, if set to true, then the predicate
        will look at all columns excluding the one(s) specified in column_names
        :type column_names_exclude: bool
        """

        if isinstance(table_name, str):
            self.table_name = [table_name]
        else:
            self.table_name = table_name

        self.column_names = column_names
        self.duplicates = []
        self.table = None
        self.columns = None
        self.column_names_exclude = column_names_exclude

    def run(self, dw_rep):
        """
        Checks for duplicates using a hash table. Each time a row is met,
        we hash it into the table. If the same row has already been hashed
        a duplicate has been found and we register it.
        :param dw_rep: DWRepresentation
        :return: report object
        """

        # Gets the columns to iterate over
        chosen_columns = self.setup_columns(dw_rep, self.table_name,
                                            self.column_names,
                                            self.column_names_exclude)

        join_column_list = []
        for table in self.table_name:
            all_columns = set(dw_rep.get_data_representation(table).all)
            join_column_list.append(all_columns)

        join_attributes = set.intersection(*join_column_list)

        pred_sql = \
            " SELECT " + ",".join(join_attributes) + " ,COUNT(*)" + \
            " FROM " + " NATURAL JOIN ".join(self.table_name) + \
            " GROUP BY " + ",".join(chosen_columns) + \
            " HAVING COUNT(*) > 1 "
        cursor = dw_rep.connection.cursor()
        cursor.execute(pred_sql)
        query_result = cursor.fetchall()

        if not query_result:
            self.__result__ = True

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=query_result,
                      msg=None)
