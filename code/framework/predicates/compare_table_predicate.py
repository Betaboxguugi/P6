__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from itertools import filterfalse
from .predicate import Predicate
from .predicate_report import Report


def difference(a, b):
    """ Equivalent to A-B or A\B in set theory. Difference/Relative Complement
    """
    return list(filterfalse(lambda x: x in b, a))


class CompareTablePredicate(Predicate):
    def __init__(self, actual_name, expected_table,
                 ignore_atts=None, subset=False):
        """
        :param actual_name: Name of the table from dw to compare with
        :param expected_table: List of dicts for table to compare against
        :param ignore_atts: List of attributes that we wish to ignore
        :param subset: Boolean, if True, it checks if the expected table is a 
        subset of the actual table.
        """

        # Fetching the DW table through its name
        self.ignore_atts = ignore_atts
        self.actual_name = actual_name
        self.expected_table = expected
        self.subset = subset
        self.incorrect_entries = []
        
    def run(self, dw_rep):
        """
        Compares the two tables and sets their surpluses for reporting.
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


        result = []
        if self.subset:
            result = difference(expected, actual)
        else:
            result = difference(actual, expected)
            result += difference(expected, actual)



        self.incorrect_entries = result
        if len(result) == 0:
            self.result = True
        else:
            self.result = False

    def report(self):
        """
        Reports results of tests.
        If it fails it will print tuples with no match.
        """

        return Report(name_of_predicate=self.__class__.__name__,
                      result=self.__result__,
                      message_if_true='Correct',
                      message_if_false='Error',
                      list_of_wrong_elements=self.incorrect_entries
                      )
