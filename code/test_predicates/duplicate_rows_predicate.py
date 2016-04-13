from test_predicates.t_predicate import TPredicate


class DuplicatePredicate(TPredicate):

    def __init__(self, table_name=None, column_names=None, verbose=False):
        """
        :param table_name: If not provided, a random table will be selected. This won't matter if there is only one
        table.
        :type table_name: str
        :param column_names: Optional parameter. A list of column names. Recommended for when you want to check for
        duplicates without looking at primary keys for example.
        :type column_names: List[str]
        :param verbose: if this is set to true information from each step in remove_unique is printed, this is for
        debugging purposes.
        :type verbose: bool
        """
        self.table_name = table_name
        self.column_names = column_names
        self.duplicates = []
        set(self.duplicates)
        self.verbose = verbose
        self.table = None
        self.columns = None
        self.dw_rep = None

    def run(self, dw_rep):
        self.dw_rep = dw_rep
        if self.table_name:
            self.table = self.dw_rep.get_data_representation(self.table_name)
        else:
            keys = list(self.dw_rep.keys())
            self.table = self.dw_rep[keys.__getitem__(0)]
        if not self.column_names:
            row = self.table.__getitem__(0)  # if no columns are given we collect them from the first row
            self.columns = row.keys()
        else:
            self.columns = self.column_names  # Otherwise we check for duplicates with the columns specified

        table = []
        for e in self.table:
            table.append(e)

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
                    x = dic.get(column.upper())
                    y = row.get(column.upper())
                    if self.verbose:
                        print("Looking at column '{}'".format(column))
                        print("Looking for value {} with key '{}'".format(x, column))
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
