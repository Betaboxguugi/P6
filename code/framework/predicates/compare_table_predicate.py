__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'
from itertools import filterfalse
from .predicate import Predicate
from .report import Report
from ..reinterpreter.datawarehouse_representation import DimRepresentation, \
    FTRepresentation
from operator import itemgetter


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

        only_in_actual = []
        only_in_expected = []

        chosen_columns = self.setup_columns(dw_rep, self.actual_table,
                                            self.column_names,
                                            self.column_names_exclude)

        # If user does not give us anything to sort on, we try to find
        # something for the sort. This can be done if all sortable keys
        # from each table is present in the join.
        # If we find some keys not intact we will not sort.
        if not self.sorted:
            for table_name in self.actual_table:
                table = self.dw_rep.get_data_representation(table_name)

                # For dimensions we can either sort on key or lookupatts
                if isinstance(table, DimRepresentation):
                    if set(table.key).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.key))
                    elif set(table.lookupatts).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.lookupatts))
                    else:
                        self.sorted.clear()
                        break
                # For fact tables we can sort on keyrefs
                elif isinstance(table, FTRepresentation):
                    if set(table.keyrefs).issubset(set(chosen_columns)):
                        self.sorted.add(set(table.keyrefs))
                    else:
                        self.sorted.clear()
                        break

            # If we can sort. TODO: Distinct.
            if self.sorted:

                actual_table_sql = \
                    "SELECT  " + ",".join(chosen_columns) + \
                    "FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    "ORDER BY " + ",".join(self.sorted)

                actual_cursor = dw_rep.conncection.cursor()
                actual_cursor.execute(actual_table_sql)

                if all(isinstance(n, str) for n in self.expected_table):

                    expected_table_sql = \
                        "SELECT  " + ",".join(chosen_columns) + \
                        "FROM " + " NATURAL JOIN ".join(
                            self.expected_table) + \
                        "ORDER BY " + ",".join(self.sorted)

                    expected_cursor = dw_rep.conncection.cursor()
                    expected_cursor.execute(expected_table_sql)

                    if not self.subset:
                        # We iterate over each table one by one comparing
                        # their rows. Any non match is logged.
                        while True:
                            a_row = actual_cursor.fetchone()
                            e_row = expected_cursor.fetchone()

                            if a_row is None and e_row is None:
                                break
                            elif a_row is None and e_row is not None:
                                only_in_expected.append\
                                    (expected_cursor.fetchall())
                                break
                            elif a_row is not None and e_row is None:
                                only_in_actual.append\
                                    ((actual_cursor.fetchall()))
                                break
                            else:
                                if a_row != e_row:
                                    only_in_actual.append(a_row)
                                    only_in_expected.append(e_row)

                        else: #subset
                            # We iterate over expected table.
                            # If entries aren't equal we see if the expected
                            # row is in a lower sort order than actual.
                            # If this occurs we know that no match for
                            # e_row exists and we move onto looking for the next

                            e_rows = expected_cursor.fetchall()
                            e_row = e_rows.pop(0)
                            while True:
                                a_row = actual_cursor.fetchone()

                                if e_row is None:
                                    break
                                elif a_row is None and e_row is not None:
                                    only_in_expected.append\
                                        (expected_cursor.fetchall())
                                else:

                                    if a_row == e_row:
                                        if e_rows:
                                           e_row = e_rows.pop(0)
                                        else:
                                            e_row = None
                                    else:
                                        a_values = {k: a_row[k] for k in
                                                    chosen_columns}.values()

                                        e_values = {k: e_row[k] for k in
                                                    chosen_columns}.values()

                                        if e_values < a_values:
                                            only_in_expected.append(e_row)
                                            if e_rows:
                                                e_row = e_rows.pop(0)
                                                if a_row == e_row:
                                                     if e_rows:
                                                        e_row = e_rows.pop(0)
                                            else:
                                                e_row = None

                # If expected table is a dictiornay
                elif all(isinstance(n, dict) for n in self.expected_table):
                    self.expected_table = \
                        sorted(self.expected_table,
                               key=itemgetter(*self.sorted))

                    if self.subset:

                    else:


            # If we cannot sort. For when expected is a table.
            else:

                # If user wants to treat entries as distinct
                if self.distinct:
                    where_sql = []
                    for name in chosen_columns:
                        equal_sql = "actual." + name + " = " + \
                                    "expected." + name
                        where_sql.append(equal_sql)

                    sql = \
                    " SELECT DISTINCT * " + \
                    " FROM " + ",".join(self.expected_table) +\
                    " AS expected " + \
                    " WHERE NOT EXISTS" \
                    "( " + \
                    "SELECT NULL " + \
                    " FROM "  + ",".join(self.actual_table)\
                    + " AS actual " + \
                    " WHERE " + ",".join(where_sql) + \
                    " )"

                    cursor = dw_rep.conncection.cursor()
                    cursor.execute(sql)
                    only_in_expected.append(cursor.fetchall())

                    if not self.subset:
                        sql = \
                        " SELECT DISTINCT * " + \
                        " FROM " + ",".join(self.actual_table) +\
                        " AS actual " + \
                        " WHERE NOT EXISTS" \
                        "( " + \
                        "SELECT NULL " + \
                        " FROM "  + ",".join(self.expected_table)\
                        + " AS expected " + \
                        " WHERE " + ",".join(where_sql) + \
                        " )"

                        cursor = dw_rep.conncection.cursor()
                        cursor.execute(sql)
                        only_in_actual.append(cursor.fetchall())


                # If duplicates have to be treated
                else:
                    # all(True if listA.count(item)
                    #  <= listB.count(item) else False for item in listA)

                    if self.subset:
                    else



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
"""
