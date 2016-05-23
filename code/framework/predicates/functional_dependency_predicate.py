from .predicate import Predicate
from .report import Report

__author__ = 'Alexander Brandborg'
__maintainer__ = 'Mikael Vind Mikkelsen'


class FunctionalDependencyPredicate(Predicate):
    """ Predicate that can check if a table or a join of table_names holds a certain
    functional dependency.
    """
    def __init__(self, table_names, alpha, beta):
        """
        :param table_names: table_names from the database, which we wish to join
        :param alpha: alpha which are depended upon by other
        alpha. Given as either a single attribute name, or a tuple of
        attribute names.
        :param beta: alpha which are functionally
        dependent on the former alpha. Given as either a single attribute
        name, or a tuple of attribute names.
        Example:
        alpha = ('a','b') and beta = 'c'
        corresponds to the functional dependency: a, b -> c
        """
        self.table_names = table_names
        self.alpha = alpha
        self.beta = beta
        self.results = True

    def run(self, dw_rep):
        """
        :param dw_rep: a DWRepresentation object
        Checks whether each function dependency holds.
        """

        # SQL setup for the tables specified
        if len(self.table_names) == 1 or isinstance(self.table_names, str):
            join_sql = "{} as t1 , {} as t2".format(self.table_names[0],
                                                    self.table_names[0])
        else:
            joined_sql = " NATURAL JOIN ".join(self.table_names)
            join_sql = "({}) as t1 , ({}) as t2".format(joined_sql, joined_sql)

        # Determining our dependencies, where alpha is the left side and beta
        # the right side of the dependency (alpha --> beta)
        alpha = self.alpha
        beta = self.beta

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
                               for x in range(0, len(alpha)))
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
        lookup_sql = "SELECT DISTINCT " + select_sql + " FROM " + join_sql +\
                     " WHERE " + and_alpha + " AND " + "( {} )".format(or_beta)
        func_dep = "{} --> {}".format(alpha, beta)
        cursor = dw_rep.connection.cursor()
        cursor.execute(lookup_sql)
        tuples = cursor.fetchall()
        names = [t[0] for t in cursor.description]
        elements = []
        # If the SQL command returns rows that fail against the dependency if
        # any.
        for row in tuples:
            elements.append(dict(zip(names, row)))
            self.results = False

        return Report(result=self.results,
                      elements=elements,
                      tables=self.table_names,
                      predicate=self,
                      msg='The predicate failed for the functional '
                          'dependency "{}" \n'
                          ' |  It did not hold on the following elements:'.
                      format(func_dep))
