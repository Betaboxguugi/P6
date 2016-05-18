from .predicate import Predicate
from .report import Report

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg'


def ref_sql(table1, table2, key):
        """
        Create SQL for checking referential in one way.
        If result not empty, the integrity does not hold.
        :param table1: Main table
        :param table2: Foreign key table
        :param key: Key between the tables
        :return: Resulting sql string
        """

        sql = \
            " SELECT * " + \
            " FROM " + table1.name + \
            " WHERE NOT EXISTS" \
            "( " + \
            "SELECT NULL " + \
            " FROM " + table2.name + \
            " WHERE " + table1.name + "." + key + \
            " = " \
            + table2.name + "." + key + \
            " )"
        return sql


def referential_check(table1, table2, key, dw_rep):
        """
        Produces and runs query checking referential integrity one way
        :param table1: Main table
        :param table2: Foreign key table
        :param key: Key between the tables
        :param dw_rep: Representation of DW
        :return: Query result
        """

        # Creates query
        table_to_dim_sql = ref_sql(table1, table2, key)

        # Run query and return result
        cursor = dw_rep.connection.cursor()
        cursor.execute(table_to_dim_sql)

        query_result = cursor.fetchall()
        cursor.close()
        return query_result


class ReferentialIntegrityPredicate(Predicate):
    """
    Checks referential integrity between tables.
    Treats all tables as distinct.
    """

    def __init__(self, refs={}, table_one_to_many=True,
                 dim_one_to_many=True):
        """
        :param refs: Dictionary with table pairs to perform check between
        :param table_one_to_many: If true. We check that for each entry in
        the main table that there is a match at the foreign key table.
        :param dim_one_to_many: If true. We check that for each entry in
        the foreign table that there is a match at the main table.
        :return:
        """
        self.table_one_to_many = table_one_to_many
        self.dim_one_to_many = dim_one_to_many
        self.refs = refs
        self.dw_rep = None
        if not table_one_to_many and not dim_one_to_many:
            raise RuntimeError("Both table_one_to_many"
                               " and dim_one_to_many can not be set to false")

    def run(self, dw_rep):

        missing_keys = []

        # If references not given. We check refs between all tables.
        if not self.refs:
            self.refs = dw_rep.refs

        # Performs check for each pair of main table and foreign key table.
        for table, dims in self.refs.items():
            for dim in dims:
                key = dim.key

                # Check that each entry in main table has match
                if self.table_one_to_many:
                    query_result = referential_check(table, dim,
                                                     key, dw_rep)

                    if query_result:
                        missing_keys.append(query_result)

                # Check that each entry in foreign key table has match
                if self.dim_one_to_many:
                    query_result = referential_check(dim, table,
                                                     key, dw_rep)

                    if query_result:
                        missing_keys.append(query_result)

        if not missing_keys:
            self.__result__ = True

        # Get names of main tables
        names = []
        for key in self.refs.keys():
            names.append(key.name)

        return Report(result=self.__result__,
                      tables=names,
                      predicate=self,
                      elements=missing_keys
                      )


