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
        self.results = []
        self.ignore_none = ignore_none


    def run(self, dw_rep):
        """
        Checks whether each function dependency holds.
        Uses a dictionary as a hash table. For each functional dependency,
        it keeps of pairings of alpha and beta values. If we find several
        beta values for one alpha, we register an error.
        """
        hts = [{} for fd in self.func_dependencies]
        elements = []

        for row in dw_rep.iter_join(self.tables): # Natural join of tables
            for idx, fd in enumerate(self.func_dependencies):
                alpha = (row[x] for x in fd[0])
                beta = (row[y] for y in fd[1])

                if self.ignore_none and any(x is None for x in alpha):
                    pass
                # If the FD doesn't hold
                elif alpha in hts[idx] and hts[idx][alpha] != beta:
                    elements.append((fd, row))
                # If we haven't met alpha before
                elif alpha not in hts[idx]:
                    hts[idx][alpha] = beta

        result = not elements
        return Report(result=result,
                      tables=self.tables,
                      predicate=self,
                      elements=elements,
                      msg='The predicate failed for the following rows,'
                          ' given as (predicate, row) tuples')
