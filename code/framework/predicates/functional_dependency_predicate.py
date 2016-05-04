__author__ = 'Alexander Brandborg'
__maintainer__ = 'Mathias Claus Jensen'
from .predicate import Predicate
from .report import Report


class FunctionalDependencyPredicate(Predicate):
    """ Predicate that can check if a table or a join of tables holds certain
    functional dependencies.
    """
    
    def __init__(self, tables, fds, ignore_None=False):
        """
        :param tables: tables from the database, which we wish to join
        :param fds: functional dependencies between attributes, given
        as a list of tubles. E.g. [('a', 'b'), ('a', 'c')], i.e. a -> b and a -> c
        :param ignore_none: Boolean, if true then we dont care what None values point at.
        """

        self.cursor = None
        self.tables = tables
        self.fds = fds
        self.results = []

    def run(self, dw_rep):
        """
        """
        hts = [{} for fd in self.fds] # Hash Tables
        elements = [] # Errorneous elements

        for row in dw_rep.iter_join(self.tables): # Natural join of tables
            for idx, fd in enumerate(self.fds):
                x = row[fd[0]] 
                y = row[fd[1]]
                
                if self.ignore_None and x == None:
                    pass
                elif x in hts[idx] and hts[idx][x] != y: # If the FD doesn't hold
                    elements.append((fd, row))
                elif x in hts[idx]: # If we've seen this value before
                    pass
                else:
                    hts[idx][x] = y # If we haven't

        result = not elements
        return Report(result=result,
                      predname='FunctionalDependencyPredicate',
                      elements=elements)
                        
            
