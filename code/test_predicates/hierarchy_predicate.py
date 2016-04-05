__author__ = 'Alexander'

import sqlite3
import pygrametl
from t_predicate import TPredicate

class HierarchyPredicate(TPredicate): # TODO: Make this shit handle nulls

    def run(self):
        """ Creates SQL for checking functional dependencies, runs it and saves results """

        sql_union = []

        # Loop for iterating over each functional dependency.
        # The SQL created for a functional dependency will return an empty table,
        # if the functional dependency is uphold.
        for func_dep_id, func_dep in enumerate(self.func_dependencies):
            alpha = func_dep[0]
            beta = func_dep[1]

            # Creates the alpha part of the where clause.
            alpha_sql = set()
            for a in alpha:
                alpha_sql.add(" A." + a + "=B." + a + " ")

            s = " AND "
            where_alpha = s.join(alpha_sql)

            # Creates the beta part of the where clause.
            t = " OR "
            beta_sql = set()
            for b in beta:
                beta_sql.add(" A." + b + "<>B." + b + " ")

            where_beta = t.join(beta_sql)

            # Creates the entire SQL statement for the functional dependency
            func_dep_sql = "SELECT *, " + str(func_dep_id) + "  FROM Big AS A, Big AS B " \
                                                             "WHERE" + where_alpha + " AND (" + where_beta + ")"
            sql_union.append(func_dep_sql)

        # Unions all SQL statements for each funcional dependency
        func_dep_sql = " UNION ".join(sql_union)

        # Creats the SQL statement for joining together our tables.
        join_table_sql = "SELECT * FROM " + " NATURAL JOIN ".join(self.tables)

        # SQL for join table is given an alias so it need only be calculated once.
        with_sql = "WITH Big AS(" + join_table_sql + ") "

        # The final SQL statement is created, executed and results are fetched.
        final_sql = with_sql + "SELECT * FROM (" + func_dep_sql + ")"
        self.cursor.execute(final_sql)
        faulty_entry_list = self.cursor.fetchall()

        # Filling up result list.
        # Each entry corresponds to the result of a specefic functional dependency.
        self.results = [True] * len(self.func_dependencies)

        # Creates a sorted list of ids, relating to functional dependencies not upheld.
        error_id_list = sorted([x[-1] for x in faulty_entry_list])

        # Iterates through the error list and reports functional dependencies not upheld.
        current_id = -1
        for err_id in error_id_list:
            res = err_id
            if res != current_id:
                current_id = res
                self.results[res] = False

    def report(self):
        """ Prints the list of results """

        for id, res in enumerate(self.results):
            func_dependency = self.func_dependencies[id]
            print(",".join(func_dependency[0]) + " --> " + ",".join(func_dependency[1]) + " : " + str(res))

    def __init__(self, connection, tables, func_dependencies):
        """
        :param connection: a connection object to a database, which we fetch data from.
        :param tables: tables from the database, which we wish to join
        :param func_dependencies: functional dependencies between attributes
        """

        self.connection = connection
        self.cursor = self.connection.cursor()
        self.tables = tables
        self.func_dependencies = func_dependencies
        self.results = []

        self.run()
        self.report()