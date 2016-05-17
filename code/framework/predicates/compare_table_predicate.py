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

def grouped_sql(table,columns):
    sql = \
        " ( " + \
        "SELECT " + ",".join(columns) + ", COUNT(*) " + \
        "AS COUNT " + \
        " FROM " + ",".join(table) + \
        " GROUP BY " + ",".join(columns) + \
        " ) "
    return sql


def unsorted_not_distinct(table1, table2, subset=False):
    only_in_table1 = []
    if subset:
        for row in table1:
            if table1.count(row) > table2.count(row):
                only_in_table1.append(row)

    else:
        for row in table1:
            if table1.count(row) != table2.count(row):
                only_in_table1.append(row)

    return only_in_table1


def tab_unsorted(table1, table2, where_conditions, dw_rep):
    sql = \
        " SELECT  * " + \
        " FROM " + table1 + \
        " AS table1 " + \
        " WHERE NOT EXISTS" \
        " ( " + \
        " SELECT NULL " + \
        " FROM " + table2 + \
        " AS table2 " + \
        " WHERE " + " AND ".join(where_conditions) + \
        " ) "

    cursor = dw_rep.connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


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
                        self.sort_keys = self.sort_keys.union(
                            set(table.keyrefs))

                    else:  # In the case that sort key of table is not present
                        self.sort_keys.clear()
                        break

        if self.expected_in_db:  # When expected is in DW

            if self.sort_keys and self.sort: # Sorted comparison
                if self.distinct:
                    select_sql = " SELECT DISTINCT "
                else:  # not distinct
                    select_sql = " SELECT "

                # Query for getting actual table sorted on keys
                actual_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                print(actual_table_sql)
                actual_cursor = dw_rep.connection.cursor()
                actual_cursor.execute(actual_table_sql)

                # Query for getting expected table sorted on keys
                expected_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(
                        self.expected_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                print(expected_table_sql)
                expected_cursor = dw_rep.connection.cursor()
                expected_cursor.execute(expected_table_sql)

                if self.subset:
                    raise RuntimeError('Cannot perform subset check on sorted')

                else:
                    only_in_actual, only_in_expected = \
                        sorted_compare(actual_cursor, expected_cursor)

            else:  # Unsorted comparison
                where_set = set(chosen_columns)
                where_conditions = []
                for name in where_set:
                    equal_sql = "table1." + name + " = " + "table2." + name
                    where_conditions.append(equal_sql)


                if self.distinct:
                    actual_sql = ",".join(self.actual_table)
                    expected_sql = ",".join(self.expected_table)

                else:  # not distinct
                    actual_sql = grouped_sql(self.actual_table,
                                             chosen_columns)

                    expected_sql = grouped_sql(self.expected_tablee,
                                               chosen_columns)
                    if self.subset:
                        sql_count = " table1.COUNT <= table2.COUNT "
                    else:
                        sql_count = " table1.COUNT =  table2.COUNT"
                    where_conditions.append(sql_count)

                if not self.subset:
                    # Get all entries only in expected
                    expected_query = \
                        tab_unsorted(expected_sql, actual_sql,
                                     where_conditions, dw_rep)
                    if expected_query:
                        only_in_expected = expected_query

                    # Get all entries only in actual
                    actual_sql_query = \
                        tab_unsorted(actual_sql, expected_sql,
                                     where_conditions, dw_rep)
                    if actual_sql_query:
                        only_in_actual = actual_sql_query

                if self.subset:
                    # Get all entries only in expected
                    expected_query = \
                        tab_unsorted(expected_sql, actual_sql,
                                     where_conditions, dw_rep)
                    if expected_query:
                        only_in_expected = expected_query

        else:  # Expected table as dicts
            # Extracts only columns to compare from expected
            self.expected_table = \
                [{k: v for k, v in d.items() if k in chosen_columns}
                 for d in self.expected_table]

            if self.sort:  # Sorted compare
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

                # Sort actual table in SQL and fetch
                actual_table_sql = \
                    select_sql + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table) + \
                    " ORDER BY " + ",".join(self.sort_keys)

                actual_cursor = dw_rep.connection.cursor()
                actual_cursor.execute(actual_table_sql)

                # Sort expected table
                expected_dict = \
                    sorted(self.expected_table,
                           key=itemgetter(*self.sort_keys))

                if self.subset:
                    raise RuntimeError('Cannot perform subset check on sorted')
                else:
                    only_in_actual, only_in_expected = \
                        sorted_compare(actual_cursor, expected_dict)

            else:  # Unsorted compare

                # Fetch contents of actual
                actual_table_sql = \
                    " SELECT " + ",".join(chosen_columns) + \
                    " FROM " + " NATURAL JOIN ".join(self.actual_table)
                cursor = dw_rep.connection.cursor()
                cursor.execute(actual_table_sql)
                query_result = cursor.fetchall()

                # Create dictionary from fetched tuples and attribute names
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
                        only_in_expected = unsorted_not_distinct(
                            expected_dict, actual_dict)

                        only_in_actual = unsorted_not_distinct(
                            actual_dict, expected_dict)

                    else:
                        only_in_expected = unsorted_not_distinct(
                                expected_dict,
                                actual_dict,
                                True)

        # If no non-matching rows found, the assertion held.
        all_unmatched = only_in_expected + only_in_actual
        if not all_unmatched:
            self.__result__ = True

        return Report(result=self.__result__,
                      tables="Many tables Yes",
                      predicate=self,
                      elements=all_unmatched,
                      msg=None)
