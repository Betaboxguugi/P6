from test_predicates.t_predicate import TPredicate


class DuplicatePredicate(TPredicate):

    def __init__(self, conn, table_name=None, column_names=None, verbose=False):
        """
        :param conn: a connection object to a database, which we fetch data from.
        :param table_name: If not provided, a random table will be selected. This won't matter if there is only one
        table.
        :type table_name: str
        :param column_names: Optional parameter. A tuple of column names. Recommended for when you want to check for
        duplicates without looking at primary keys for example.
        :type column_names: str
        :param verbose: if this is set to true information from each step in remove_unique is printed
        :type verbose: bool
        """
        self.database = self.dictify(conn)

        if table_name:
            self.table = self.database[table_name]
        else:
            keys = list(self.database.keys())
            self.table = self.database[keys.__getitem__(0)]
        if not column_names:
            row = self.table.__getitem__(0)  # if no columns are given we collect them from the first row
            self.columns = row.keys()
        else:
            self.columns = column_names  # Otherwise we check for duplicates with the columns specified
        self.duplicates = []
        set(self.duplicates)
        self.verbose = verbose

    def run(self):
        table = self.table
        while len(table) > 1:
            dic = table.pop(0)  # this dict(row) is the one we will check against all other rows in the table
            if self.verbose:
                print('Start predicate duplicates')
                print("Rows remaining {}".format(len(table)))
            for row in table:
                if self.verbose:
                    print("Checking table against row: {}".format(dic))
                    print("Checking table row: {}".format(row))
                flag = False
                for column in self.columns:  # Fun fact: columns may be unordered if not provided
                    x = dic.get(column)
                    y = row.get(column)
                    if self.verbose:
                        print("Looking at column {}".format(column))
                        print("Looking for value {} with key {}".format(x, column))
                        print("Found value {}".format(y))
                    if x != y:  # if two values between the rows are not duplicates, the rows are not duplicates,
                        if self.verbose:  # and we don't care about the rest of the values in those rows
                            print('Unique')
                        flag = False
                        break  # exit the for loop, this should bring us to the next row in the outer for loop
                    else:
                        if self.verbose:
                            print('Duplicate value')
                        flag = True
                if flag and dic not in self.duplicates:  # duplicates is a set and we check if we have already noted
                    if self.verbose:                     # this duplicate row
                        print('Duplicate row found')
                    self.duplicates.append(dic)
                if flag and row not in self.duplicates:
                    self.duplicates.append(row)
        if len(self.duplicates) < 1:
            self.__result__ = True
        self.report()

    def report(self):
        if not self.__result__:
            print(self.duplicates)
        print(self.__result__)
