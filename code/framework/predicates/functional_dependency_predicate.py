__author__ = 'Alexander Brandborg'
__maintainer__ = 'Mikael Vind Mikkelsen'
from .predicate import Predicate
from .report import Report


class FunctionalDependencyPredicate(Predicate):
    """ Predicate that can check if a table or a join of tables holds certain
    functional dependencies.
    """
    def __init__(self, tables, func_dependencies):
        """
        :param tables: tables from the database, which we wish to join
        :param func_dependencies: functional dependencies between attributes,
        given as a list of tuples.
         E.g. [(('a'), ('b')), (('a','b'), ('c'))], i.e. a -> b and a,b -> c
        """
        self.tables = tables
        self.func_dependencies = func_dependencies
        self.results = True

    def run(self, dw_rep):
        """
        Checks whether each function dependency holds.
        Uses a dictionary as a hash table. For each functional dependency,
        it keeps of pairings of alpha and beta values. If we find several
        beta values for one alpha, we register an error.
        """

        # SQL setup for the tables specified
        if len(self.tables) == 1 or isinstance(self.tables, str):
            join_sql = "{} as t1 , {} as t2".format(self.tables[0], self.tables[0])
        else:
            joined_sql = " NATURAL JOIN ".join(self.tables)
            join_sql = "({}) as t1 , ({}) as t2".format(joined_sql, joined_sql)

        # Determining our dependencies, where alpha is the left side and beta
        # the right side of the dependency (alpha --> beta)
        alpha = self.func_dependencies[0]
        beta = self.func_dependencies[1]

        # SQL setup for first part of SELECT, which are the left side of
        # the dependencies
        select_alpha_sql_generator = (" t1.{} ".format(alpha[x])
                                      for x in range(0, len(alpha)))
        if len(alpha) == 1 or isinstance(alpha, str):
            select_sql_alpha = "t1.{}".format(alpha)
        else:
            select_sql_alpha = ",".join(select_alpha_sql_generator)

        # SQL setup for second part of SELECT, which are the right side of
        # the dependencies
        select_beta_sql_generator = (" t1.{} ".format(beta[x])
                                     for x in range(0, len(beta)))
        if len(beta) == 1 or isinstance(beta, str):
            select_sql_beta = "t1.{}".format(beta)
        else:
            select_sql_beta = ",".join(select_beta_sql_generator)

        # SQL setup for the whole SELECT portion. Used to only show relevant
        # columns when reporting to the user.
        select_sql = select_sql_alpha + " ," + select_sql_beta

        # SQL setup for the left side of the dependency
        alpha_sql_generator = (" t1.{} = t2.{} ".format(alpha[x], alpha[x])
                               for x in range(0,len(alpha)))
        if len(alpha) == 1 or isinstance(alpha, str):
            and_alpha = " t1.{} = t2.{} ".format(alpha, alpha)
        else:
            and_alpha = ' AND '.join(alpha_sql_generator)

        # SQL setup for the right side of the dependency
        beta_sql_generator = (" (t1.{} <> t2.{}) ".format(beta[x], beta[x])
                               for x in range(0, len(beta)))
        if len(beta) == 1 or isinstance(beta, str):
            or_beta = " (t1.{} <> t2.{}) ".format(beta, beta)
        else:
            or_beta = ' OR '.join(beta_sql_generator)

        # Final setup of the entire SQL command
        lookup_sql = "SELECT " + select_sql + " FROM " + join_sql +\
                     " WHERE " + and_alpha + " AND " + "( {} )".format(or_beta)
        
        func_dep = "{} --> {}".format(alpha, beta)
        c = dw_rep.connection.cursor()
        c.execute(lookup_sql)
        elements = set()

        # If the SQL command returns rows that fail against the dependencies if
        # any.
        for row in c.fetchall():
            elements.add(row)
            self.results = False

        return Report(result=self.results,
                      elements=elements,
                      tables=self.tables,
                      predicate=self,
                      msg='The predicate failed for the functional dependencie "{}" \n' \
                     ' |  It did not hold on the following elements:'.format(func_dep))
