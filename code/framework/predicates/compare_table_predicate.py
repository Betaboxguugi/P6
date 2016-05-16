__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from itertools import filterfalse
from .predicate import Predicate
from .report import Report
from ..reinterpreter.datawarehouse_representation import DimRepresentation, \
    FTRepresentation
from operator import itemgetter


def difference(a, b):
    """
    Equivalent to A-B or A\B in set theory. Difference/Relative Complement
    :param a: First list of dicts
    :param b: Second list of dicts
    :return: List of elements in a but not in b
    """
    return list(filterfalse(lambda x: x in b, a))


def get_next_row(table, names):
    """
    Used to get next row of either list of dicts or cursor
    :param table: Table to get next row from
    :return: Next row
    """

    if isinstance(table, list):
        if not table:
            return None, True
        else:
            return table.pop(0), False
    else:
        row = table.fetchone()
        if row is None:
            return None, True
        else:
            return dict(zip(names, row)), False


def get_rest_of_table(table, names):
    """
    Fetches the rest of a table that's either list of dicts or a cursor
    :param table: table to fetch from
    :return: Rest of rows as a list of dicts
    """
    if isinstance(table, list):
        return table
    else:
        result = []
        for row in table.fetchall():
            result.append(dict(zip(names, row)))

        return result


def table_is_empty(table, row):
    """
    To check whether a given table contains more rows
    :param table: table to check
    :param row: current row
    :return: True if empty, else False.
    """

    if isinstance(table, list):
        return not table
    else:
        return row is None


def dict_unsorted_not_distinct(table1, table2, subset=False):
    only_in_table1 = []
    if (subset):
        for row in table1:
            if table1.count(row) > table2.count(row):
                only_in_table1.append(row)

    else:
        for row in table1:
            if table1.count(row) != table2.count(row):
                only_in_table1.append(row)

    return only_in_table1




def sorted_compare(actual, expected):
    """
    Does a positional comparison of two sorted tables
    :param actual: Table in DW
    :param expected: Table given by user
    :return: two lists containing exclusive rows to each table
    """
    names = [t[0] for t in actual.description]
    actual_list = []
    expected_list = []

    while True:
        a_row, actual_empty = get_next_row(actual, names)
        e_row, expected_empty = get_next_row(expected, names)

        # Does not compare any that include nulls
        # This is done to mimic results of comparing with nulls in sql
        while not actual_empty and (None in a_row.values()):
            actual_list.append(a_row)
            a_row, actual_empty = get_next_row(actual, names)

        while not expected_empty and None in e_row.values():
            expected_list.append(e_row)
            e_row, expected_empty = get_next_row(expected, names)

        if not expected_empty and not actual_empty:
            if a_row != e_row:
                actual_list.append(a_row)
                expected_list.append(e_row)

        # When the two tables are of equal length
        if actual_empty and expected_empty:
            break

        # When there's more in expected table
        elif actual_empty and not expected_empty:
            rest_list = [e_row]
            rest_list.extend(get_rest_of_table(expected, names))
            expected_list.extend(rest_list)
            break

        # When there's more in actual table
        elif not actual_empty and expected_empty:
            rest_list = [a_row]
            rest_list.extend(get_rest_of_table(actual, names))
            actual_list.extend(rest_list)
            break

    return actual_list, expected_list


def sorted_subset_compare(actual, expected, sort_columns):
    """
    Does positional compare of two tables. Checking whether one is a subset.
    :param actual: Table in DW
    :param expected: Table given by user. Always a list of dicts.
    :param compare_columns: The columns that were sorted on
    :return: List of all rows exclusive to expected
    """
    names = [t[0] for t in actual.description]

    e_row = get_next_row(expected, names)
    expected_list = []

    while True:
        a_row = get_next_row(actual, names)

        # Does not compare any that include nulls
        # This is done to mimic results of comparing with nulls in sql
        while not (table_is_empty(actual, a_row)) and (None in a_row.values()):
            a_row = get_next_row(actual, names)

        while not table_is_empty(expected, e_row) and None in e_row.values():
            expected_list.append(e_row)
            e_row = get_next_row(expected, names)

        # When expected is empty
        if table_is_empty(expected, e_row):
            break

        # When actual is empty we store the rest of the non-matching rows
        elif table_is_empty(actual, a_row) and not table_is_empty(expected,
                                                                  e_row):
            expected_list.append(get_rest_of_table(expected))

        else:
            if a_row == e_row:
                if not table_is_empty(expected):
                    e_row = get_next_row(expected)

            else:
                # If the actual table row is higher in the sort order than
                # our current expected row, then there is no match, and we
                # go onto the next row in expected.

                a_values = {k: a_row[k] for k in
                            sort_columns}.values()

                e_values = {k: e_row[k] for k in
                            sort_columns}.values()

                if e_values < a_values:
                    expected_list.append(e_row)
                    if not table_is_empty(expected):
                        e_row = get_next_row(expected, names)

                        # Quick check to see if the new expected row matches
                        # the actual row, before the next actual row is fetched
                        if a_row == e_row:
                            if not table_is_empty(expected):
                                e_row = get_next_row(expected, names)

    return expected_list


class CompareTablePredicate(Predicate):
    """ Predicate that compares two tables, actual and expected, to each other. 
    Asserting they are equivalent or that the expected is a subset of actual.
    The user can ignore specific attributes when comparing.
    """

    def __init__(self, actual_table, expected_table,
                 column_names=None, column_names_exclude=False, sort=True,
                 sort_keys=(), distinct=True, subset=False):
        """
        :param actual_table: Actual table in DW
        :param expected_table: User defined table to compare with
        :param column_names: Columns to use for comparison
        :param column_names_exclude: To get complement of column_names
        :param sort_keys: Set of attributes to sort on.
        :param distinct: If tables should be treated as having no duplicates
        :param subset: If we should check that expected_table is only a subset

        """

        # Make sure that actual table is a list of names
        if isinstance(actual_table, str):
            self.actual_table = [actual_table]
        elif isinstance(actual_table, list):
            self.actual_table = actual_table
        else:
            raise RuntimeError('Actual table not given as string'
                               ' or list of strings')

        # Make sure that expected table is a list of names
        if isinstance(expected_table, str):
            self.expected_table = [expected_table]
            self.expected_in_db = True

        # If list we check that it is either of names or dicts.
        # Also sets a flag to indicate, which one it is.
        elif isinstance(expected_table, list):
            if all(isinstance(n, dict) for n in expected_table):
                self.expected_in_db = False
            elif all(isinstance(n, str) for n in expected_table):
                self.expected_in_db = True
            else:
                raise RuntimeError('Neither list of names nor dicts given'
                                   'for expected table')
            self.expected_table = expected_table

        # If not any cases caught the input, it must be a cursor.
        # We fetch all data from it so we have a list of dicts.
        else:
            # If expected table is given as a cursor, we fetch from it
            try:
                tuples = expected_table.fetchall()
                names = [t[0] for t in expected_table.description]
                self.expected_table = []
                for row in tuples:
                    self.expected_table.append(dict(zip(names, row)))
                self.expected_in_db = False
            except Exception:
                raise RuntimeError('Expected table neither given as a name,' +
                                   'list of names, dicts nor cursor')

        self.column_names = column_names
        self.column_names_exclude = column_names_exclude
        self.sort = sort
        self.sort_keys = set(sort_keys)
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

        # Gets the actual columns we want to compare on.
        chosen_columns = self.setup_columns(dw_rep, self.actual_table,
                                            self.column_names,
                                            self.column_names_exclude)

        # If user does not give us anything to sort on, we try to find
        # something for the sort. This can be done if all sortable keys
        # from each table is present in the join.
        # If we find some keys not intact we will not sort.
        if self.sort and not self.sort_keys:

            for table_name in self.actual_table:
                table = dw_rep.get_data_representation(table_name)

                # For dimensions
                if isinstance(table, DimRepresentation):
                    # We can either sort on key or lookupatts
                    if set([table.key]).issubset(set(chosen_columns)):
                        self.sort_keys = self.sort_keys.union(set([table.key]))

                    elif set(table.lookupatts).issubset(set(chosen_columns)):
                        self.sort_keys = self.sort_keys.union(
                            set(table.lookupatts))

                    else:  # In the case that sort key of table is not present
                        self.sort_keys.clear()
                        break

                # For fact tables
                elif isinstance(table, FTRepresentation):
                    # Can sort on keyrefs
                    if set(table.keyrefs).issubset(set(chosen_columns)):
                        self.sort_keys.union = self.sort_keys(
                            set(table.keyrefs))

                    else:  # In the case that sort key of table is not present
                        self.sort_keys.clear()
                        break

        # In the case that data from expected table lies in same DB as the DW
        if self.expected_in_db:

            # If we have a set to sort on.
            if self.sort:
                if self.distinct:
                    select_sql = " SELECT DISTINCT "
                else:  # not distinct
                    select_sql = " SELECT "

                # Query for getting actual table sorted on keys
                actual_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                actual_cursor = dw_rep.connection.cursor()
                actual_cursor.execute(actual_table_sql)

                # Query for getting expected table sorted on keys
                expected_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(
                        self.expected_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                expected_cursor = dw_rep.connection.cursor()
                expected_cursor.execute(expected_table_sql)

                if not self.subset:
                    # We iterate over each table one by one comparing
                    # their rows. Any non match is logged.

                    only_in_actual, only_in_expected = \
                        sorted_compare(actual_cursor, expected_cursor)

                else:  # subset
                    # We iterate over expected table.

                    only_in_expected = \
                        sorted_subset_compare(actual_cursor,
                                              expected_cursor,
                                              self.sort_keys)

            # If we cannot sort. For when expected is a table.
            else:
                where_set = set(chosen_columns)
                where_sql = []
                for name in where_set:
                    equal_sql = "actual." + name + " = " + \
                                "expected." + name
                    where_sql.append(equal_sql)

                # If user wants to treat entries as distinct.
                # The SQL makes sure to group all identical rows, and find
                # their count.
                if self.distinct:
                    actual_sql = ",".join(self.actual_table)
                    expected_sql = ",".join(self.expected_table)

                # If we have to handle duplicates
                else:
                    actual_sql = \
                        " ( " + \
                        "SELECT " + ",".join(chosen_columns) + ", COUNT(*) " +\
                        "AS COUNT " + \
                        " FROM " + ",".join(self.actual_table) + \
                        " GROUP BY " + ",".join(chosen_columns) + \
                        " ) "

                    expected_sql = \
                        " ( " + \
                        "SELECT " + ",".join(chosen_columns) + ", COUNT(*) " +\
                        "AS COUNT " + \
                        " FROM " + ",".join(self.expected_table) + \
                        " GROUP BY " + ",".join(chosen_columns) + \
                        " ) "

                    if self.subset:
                        sql_count = " expected.COUNT = actual.COUNT "
                    else:
                        sql_count = " expected.COUNT = actual.COUNT "
                    where_sql.append(sql_count)

                    if not self.subset:
                        sql = \
                            " SELECT  * " + \
                            " FROM " + expected_sql + \
                            " AS expected " + \
                            " WHERE NOT EXISTS" \
                            " ( " + \
                            " SELECT NULL " + \
                            " FROM " + actual_sql + \
                            " AS actual " + \
                            " WHERE " + " AND ".join(where_sql) + \
                            " ) "

                        cursor = dw_rep.connection.cursor()
                        cursor.execute(sql)
                        query_result = cursor.fetchall()
                        if query_result:
                            only_in_expected = query_result

                        sql = \
                            " SELECT  * " + \
                            " FROM " + actual_sql + \
                            " AS actual " + \
                            " WHERE NOT EXISTS" \
                            " ( " + \
                            " SELECT NULL " + \
                            " FROM " + expected_sql + \
                            " AS  expected " + \
                            " WHERE " + " AND ".join(where_sql) + sql_count + \
                            " ) "

                        cursor = dw_rep.connection.cursor()
                        cursor.execute(sql)
                        query_result = cursor.fetchall()
                        if query_result:
                            only_in_actual = query_result

                    if self.subset:
                        sql = \
                            " SELECT  * " + \
                            " FROM " + expected_sql + \
                            " AS expected " + \
                            " WHERE NOT EXISTS" \
                            " ( " + \
                            " SELECT NULL " + \
                            " FROM " + actual_sql + \
                            " AS actual " + \
                            " WHERE " + " AND ".join(where_sql) + \
                            " ) "

                        cursor = dw_rep.connection.cursor()
                        cursor.execute(sql)
                        query_result = cursor.fetchall()
                        if query_result:
                            only_in_expected = query_result

        else:  # expected table as dicts

            # Cuts off all columns not used in comparison

            self.expected_table = \
                [{k: v for k, v in d.items() if k in chosen_columns}
                 for d in self.expected_table]

            if self.sort:
                if self.distinct:
                    select_sql = " SELECT DISTINCT "

                    # Remove duplicates from expected
                    expected_rows_set = \
                        set(tuple(item.items()) for item in
                            self.expected_table)
                    self.expected_table = \
                        [dict(tupleized) for tupleized in expected_rows_set]

                else:  # not distinct
                    select_sql = " SELECT "

                # Use SQL to create a cursor to the actual table
                actual_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                actual_cursor = dw_rep.connection.cursor()
                actual_cursor.execute(actual_table_sql)

                # Fetch and remove nulls from expected
                # Again this is to handle nulls in the same way as
                # would occur if we were using sql.

                expected_dict = []
                for row in self.expected_table:
                    if None in row.values():
                        only_in_expected.append(row)
                    else:
                        expected_dict.append(row)

                # Sorts expected table
                expected_dict = \
                    sorted(expected_dict,
                           key=itemgetter(*self.sort_keys))

                if not self.subset:
                    only_in_actual, only_in_expected = \
                        sorted_compare(actual_cursor, expected_dict)

                else:  # subset
                    only_in_expected = \
                        sorted_subset_compare(actual_cursor,
                                              expected_dict,
                                              self.sort_keys)

            else:

                # Get actual as list of rows
                actual_table_sql = \
                    " SELECT " + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table)
                print(actual_table_sql)
                cursor = dw_rep.connection.cursor()
                cursor.execute(actual_table_sql)
                query_result = cursor.fetchall()

                actual_dict_with_nulls = []
                names = [t[0] for t in cursor.description]
                for row in query_result:
                    actual_dict_with_nulls.append(dict(zip(names, row)))

                # Fetch and remove nulls from actual
                actual_dict = []
                for row in actual_dict_with_nulls:
                    if None in row.values():
                        only_in_actual.append(row)
                    else:
                        actual_dict.append(row)

                # Fetch and remove nulls from expected
                expected_dict = []
                for row in self.expected_table:
                    if None in row.values():
                        only_in_expected.append(row)
                    else:
                        expected_dict.append(row)

                if self.distinct:
                    # Find all rows in expected that are not in actual
                    only_in_expected = difference(expected_dict, actual_dict)

                    if not self.subset:
                        # Find all rows in actual that are not in expected
                        only_in_actual = difference(actual_dict, expected_dict)

                else:  # not distinct
                    # For each row in expected we see if the number of
                    # duplicates is the same in actual.

                    if not self.subset:
                        only_in_expected = \
                            dict_unsorted_not_distinct \
                                (expected_dict, actual_dict)

                        only_in_actual = \
                            dict_unsorted_not_distinct \
                                (actual_dict, expected_dict)

                    else:
                        only_in_expected = \
                            dict_unsorted_not_distinct \
                                (expected_dict, actual_dict, True)

        # If no non-matching rows found, the assertion held.
        all_unmatched = only_in_expected + only_in_actual
        if not all_unmatched:
            self.__result__ = True

        return Report(result=self.__result__,
                      tables="Many tables Yes",
                      predicate=self,
                      elements=all_unmatched,
                      msg=None)
