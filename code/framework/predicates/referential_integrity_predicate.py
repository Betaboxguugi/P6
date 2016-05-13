from .predicate import Predicate
from .report import Report
from framework.reinterpreter.datawarehouse_representation \
    import FTRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class ReferentialIntegrityPredicate(Predicate):
    def __init__(self, refs={}, table_one_to_many=True,
                 dim_one_to_many=True):
        self.table_one_to_many = table_one_to_many
        self.dim_one_to_many = dim_one_to_many
        self.refs = refs
        if not table_one_to_many and not dim_one_to_many:
            raise RuntimeError("Both table_one_to_many"
                               " and dim_one_to_many can not be set to false")

    def run(self, dw_rep):
        missing_keys = []

        if not self.refs:
            self.refs = dw_rep.refs

        for table, dims in self.refs.items():
            for dim in dims:
                key = dim.key

                if self.table_one_to_many:

                    table_to_dim_sql = self.outer_join_sql(table, dim, key)

                    print(self.outer_join_sql(table, dim, key))


                    cursor = dw_rep.connection.cursor()
                    cursor.execute(table_to_dim_sql)

                    query_result1 = cursor.fetchall()
                    if query_result1:
                        missing_keys.append(query_result1)

                if self.dim_one_to_many:
                    dim_to_table_sql = self.outer_join_sql(dim, table, key)

                    cursor2 = dw_rep.connection.cursor()
                    cursor2.execute(dim_to_table_sql)

                    query_result2 = cursor2.fetchall()
                    if query_result2:
                        missing_keys.append(query_result2)

        if not missing_keys:
            self.__result__ = True

        names = []
        for key in self.refs.keys():
            names.append(key.name)

        return Report(result=self.__result__,
                      tables=names,
                      predicate=self,
                      elements=missing_keys
                      )

    def ref_sql(self, table1, table2, key):

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

    def outer_join_sql(self, table1, table2, key):

        table2_att = set(table2.all).difference(set([key]))
        print(table2_att)
        null_condition_sql = (x + " IS NULL" for x in table2_att)

        sql = \
            " SELECT * " + \
            " FROM " + table1.name + " LEFT OUTER JOIN " + table2.name + \
            " ON " + table1.name + "." + key + " = " + table2.name + "." + key + \
            " WHERE " + " AND ".join(null_condition_sql)

        return sql
