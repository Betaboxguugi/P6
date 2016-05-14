__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'
from itertools import filterfalse
from .predicate import Predicate
from .report import Report
from ..reinterpreter.datawarehouse_representation import DimRepresentation, FTRepresentation


def difference(a, b):
    """ Equivalent to A-B or A\B in set theory. Difference/Relative Complement
    """
    return list(filterfalse(lambda x: x in b, a))


class CompareTablePredicate(Predicate):
    """ Predicate that compares two tables, actual and expected, to each other. 
    Asserting they are equivalent or that the expected is a subset of actual.
    The user can ignore specific attributes when comparing.
    """

    def __init__(self, actual_table, expected_table,
                 column_names=None, column_names_exclude=False,
                 sorted=(), distinct=True, subset=False):
        """
        :param actual_table: Actual table in DW
        :param expected_table: User defined table to compare with
        :param column_names: Columns to use for comparison
        :param column_names_exclude: To get complement of column_names
        :param sorted: Set of attributes to sort on.
        :param distinct: If tables should be treated as having no duplicates
        :param subset: If we should check that expected_table is only a subset

        """

        if isinstance(actual_table, str):
            self.actual_table = [actual_table]
        else:
            self.actual_table = actual_table

        if isinstance(expected_table, str):
            self.expected_table = [expected_table]
        else:
            self.expected_table = expected_table

        self.column_names = column_names
        self.column_names_exclude = column_names_exclude
        self.sorted = set(sorted)
        self.distinct = distinct
        self.subset = subset

    def run(self, dw_rep):
        """
        Compares the two tables and sets their surpluses for reporting.
        :param dw_rep: A DWRepresentation object
        :return: A Report object descriping how the predicate did
        """

        chosen_columns = self.setup_columns(dw_rep, self.actual_table,
                                            self.column_names,
                                            self.column_names_exclude)

        if not self.sorted:
            for table_name in self.actual_table:
                table = self.dw_rep.get_data_representation(table_name)

                if isinstance(table,DimRepresentation):
                    if set(table.key).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.key))
                    elif set(table.lookupatts).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.lookupatts))
                    else:
                        self.sorted.clear()
                        break
                elif isinstance(table, FTRepresentation):
                    if set(table.keyrefs).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.keyrefs))
                    else:
                        self.sorted.clear()
                        break

            if self.sorted:

                actual_table_sql = \
                    "SELECT * " + \
                    "FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    "ORDER BY " + ",".join(self.sorted)


                if isinstance(self.expected_table[0], str):
                    expected_table_sql = \
                    "SELECT * " + \
                    "FROM " + " NATURAL JOIN ".join(self.expected_table_table) + \
                    "ORDER BY " +  ",".join(self.sorted)

                elif isinstance(self.expected_table[0], dict):

                    pass





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
