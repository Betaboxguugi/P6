__author__ = 'Alexander Brandborg'
__maintainer__ = 'Mathias Claus Jensen'
from .predicate import Predicate
from .report import Report


class FunctionalDependencyPredicate(Predicate):
    """ Predicate that can check if a table or a join of tables holds certain
    functional dependencies.
    """
    def __init__(self, tables, func_dependencies, ignore_none=False):
        """
        :param tables: tables from the database, which we wish to join
        :param func_dependencies: functional dependencies between attributes,
        given as a list of tuples.
         E.g. [(('a'), ('b')), (('a','b'), ('c'))], i.e. a -> b and a,b -> c
        :ignore_none: Boolean, if true then we don't care
         what None values point at.
        """
        self.tables = tables
        self.func_dependencies = func_dependencies
        self.results = True
        self.ignore_none = ignore_none

    def run(self, dw_rep):
        """
        Checks whether each function dependency holds.
        Uses a dictionary as a hash table. For each functional dependency,
        it keeps of pairings of alpha and beta values. If we find several
        beta values for one alpha, we register an error.
        """

        if len(self.tables) == 1:
            join_sql = "{} as t1 , {} as t2".format(self.tables[0], self.tables[0])
        else:
            joined_sql = " NATURAL JOIN ".join(self.tables)
            join_sql = "({}) as t1 , ({}) as t2".format(joined_sql, joined_sql)

        alpha = self.func_dependencies[0]
        beta = self.func_dependencies[1]

        alpha_sql_generator = (" t1.{} = t2.{} ".format(alpha[x], alpha[x])
                               for x in range(0,len(alpha)))
        if len(alpha) == 1 or isinstance(alpha, str):
            and_alpha = " t1.{} = t2.{} ".format(alpha, alpha)
        else:
            and_alpha = ' AND '.join(alpha_sql_generator)

        beta_sql_generator = (" (t1.{} <> t2.{}) ".format(beta[x], beta[x])
                               for x in range(0, len(beta)))
        if len(beta) == 1 or isinstance(beta, str):
            and_beta = " (t1.{} <> t2.{}) ".format(beta, beta)
        else:
            and_beta = ' AND '.join(beta_sql_generator)

        lookup_sql = "SELECT * FROM " + join_sql + " WHERE " + and_alpha + " AND " + and_beta

        c = dw_rep.connection.cursor()
        c.execute(lookup_sql)
        if c.fetchall():
            self.results = False

        func_dep = "{} --> {}".format(alpha, beta)

        return Report(result=self.results,
                      tables=self.tables,
                      predicate=self,
                      msg='The predicate failed for the functional dependencie: {}'.format(func_dep))
