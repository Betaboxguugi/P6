__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'
from itertools import filterfalse
from .predicate import Predicate
from .report import Report


def difference(a, b):
    """ Equivalent to A-B or A\B in set theory. Difference/Relative Complement
    """
    return list(filterfalse(lambda x: x in b, a))


class CompareTablePredicate(Predicate):
    """ Predicate that compares two tables, actual and expected, to each other. 
    Asserting they are equivalent or that the expected is a subset of actual.
    The user can ignore specific attributes when comparing.
    """
    
    def __init__(self, actual_name, expected_table,
                 ignore_atts=[], subset=False):
        """
        :param actual_name: Name of the table from dw to compare with
        :param expected_table: List of dicts for table to compare against
        :param ignore_atts: List of attributes that we wish to ignore
        :param subset: Boolean, if True, it checks if the expected table is a 
        subset of the actual table.
        """
        self.ignore_atts = ignore_atts
        self.actual_name = actual_name
        self.expected_table = expected_table
        self.subset = subset
        self.incorrect_entries = []
        
    def run(self, dw_rep):
        """ Compares the two tables and sets their surpluses for reporting.
        :param dw_rep: A DWRepresentation object
        :return: A Report object descriping how the predicate did
        """
        actual = []
        expected = []     

        # Ignoring the attributes denoted in self.ignore_atts
        for entry in dw_rep.get_data_representation(self.actual_name):
            new_entry = {key: value for key, value in entry.items()
                         if key not in self.ignore_atts}
            actual.append(new_entry)
        
        for entry in self.expected_table:
            new_entry = {key: value for key, value in entry.items()
                         if key not in self.ignore_atts}
            expected.append(new_entry)    

        # We find all errorneous rows
        if self.subset: 
            errors = difference(expected, actual)
        else:
            errors = difference(actual, expected)
            errors += difference(expected, actual)

        # If errors is empty, then the predicate holds and result is equal True
        result = True
        if errors:
            result = False
            
        return Report(result=result,
                      tables=self.actual_name,
                      predicate=self,
                      elements=errors,
                      msg=None)
