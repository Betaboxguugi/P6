__author__ = 'Alexander Brandborg'
__maintainer__ = 'Mathias Claus Jensen'
from .predicate import Predicate
from .report import Report


class FunctionalDependencyPredicate(Predicate):
    # TODO: Make this shit handle nulls
    """ Predicate that can check if a table or a join of tables holds certain
    functional dependencies.
    """
    
    def __init__(self, tables, func_dependencies, ignore_none=False):
        """
        :param tables: tables from the database, which we wish to join
        :param func_dependencies: functional dependencies between attributes,
        given as a list of tuples. E.g. [('a', 'b'), ('a', 'c')], i.e. a -> b
        and a -> c
        :ignore_none: Boolean, if true then we don't care what None values
        point at.
        """

        self.cursor = None
        self.tables = tables
        self.func_dependencies = func_dependencies
        self.results = []
        self.ignore_None = ignore_none

    def run(self, dw_rep):
        """
        """
        vd = [{} for fd in self.func_dependencies]
        elements = []

        for row in dw_rep.iter_join(self.tables): # Natural join of tables
            for idx, fd in enumerate(self.func_dependencies):
                x = row[fd[0]] 
                y = row[fd[1]]
                
                if self.ignore_None and x == None:
                    pass
                elif x in vd[idx] and vd[idx][x] != y: # If the FD doesn't hold
                    elements.append((fd, row))
                elif x in vd[idx]:  # If we've seen this value before
                    pass
                else:
                    vd[idx][x] = y  # If we haven't

        result = not elements
        return Report(result=result,
                      tables=self.tables,
                      predicate=self,
                      elements=elements,
                      msg='The predicate failed for the following rows, given '
                          'as (predicate, row) tubles')
