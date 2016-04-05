from test_predicates.t_predicate import TPredicate


class ReferentialPredicate(TPredicate):

    def __init__(self, conn, referring_table_name, referred_table_name, key):
        """
        :param conn: you know by now
        :param referring_table_name: Name of the table we are checking for referential integrity, the predicate is false
        if there exists one key without a reference in the other table.
        :param referred_table_name: Name of the table that should contain references to the keys in the former table,
        the method also tests the 'reverse' integrity of this table
        :param key: name of the key or ID that is tested for referential integrity
        """
        self.warehouse = self.dictify(conn)
        self.missing_keys = ()
        self.referring_table_name = referring_table_name
        self.referred_table_name = referred_table_name
        self.key = key
        self.referring_table = self.warehouse.get(referring_table_name)
        self.referred_table = self.warehouse.get(referred_table_name)

    def run(self):
        self.__result__ = True
        self.ref_check()   # We first check the 'referring' table with the 'referred'
        self.report()
        self.swap_tables()  # we swap the two tables and do it the other way around
        self.ref_check()
        self.report()
        print(self.__result__)
        self.swap_tables()

    def swap_tables(self):
        self.referred_table, self.referring_table = self.referring_table, self.referred_table
        self.referred_table_name, self.referring_table_name = self.referring_table_name, self.referred_table_name

    def ref_check(self):
        self.missing_keys = ()  # This is reset to make sure we do not report keys from a previous check
        for referring_row in self.referring_table:
            flag = False
            for referred_row in self.referred_table:
                x = referring_row[self.key]
                y = referred_row[self.key]
                if x == y:
                    flag = True  # We find a reference match
                    break        # And immediately break out of the inner for and continue
            if not flag:
                self.missing_keys += referring_row,  # we note rows that missed their reference in the other table
                self.__result__ = False

    def report(self):
        flag = True
        for row in self.missing_keys:  # if missing_keys is empty this code will not run
            flag = False
            print("row {} in '{}' table does not have corresponding reference '{}' in '{}' table".format(
                row,
                self.referring_table_name,
                self.key,
                self.referred_table_name))
        if flag:
            print("No rows in '{}' table are missing a reference in table '{}' for '{}'".format(
                self.referring_table_name,
                self.referred_table_name,
                self.key))




