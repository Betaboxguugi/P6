from test_predicates.t_predicate import TPredicate


class ReferentialPredicate(TPredicate):

    def __init__(self, conn):
        """
        :param conn: you know by now
        """
        self.warehouse = self.dictify(conn)
        self.referring_table = []
        self.referred_table = []
        self.missing_keys = ()
        self.referring_table_name = ''
        self.referred_table_name = ''
        self.key = ''

    def run(self, referring_table_name, referred_table_name, key):
        """
        :param referring_table_name: Name of the table we are checking for referential integrity, the predicate is false
        if there exists one key without a reference in the other table.
        :param referred_table_name: Name of the table that should contain references to the keys in the former table,
        the method does not test referential integrity of this table. Recommend calling run() again with the table names
        reversed.
        :param key: name of the key or ID that is tested for referential integrity
        """
        self.referring_table_name = referring_table_name
        self.referred_table_name = referred_table_name
        self.key = key
        self.referring_table = self.warehouse.get(referring_table_name)
        self.referred_table = self.warehouse.get(referred_table_name)
        self.missing_keys = ()
        self.__result__ = True
        for referring_row in self.referring_table:
            flag = False
            for referred_row in self.referred_table:
                x = referring_row[key]
                y = referred_row[key]
                if x == y:
                    flag = True
                    break
            if not flag:
                self.missing_keys += referring_row,
                self.__result__ = False
        self.report()

    def report(self):
        if not self.__result__:
            for row in self.missing_keys:
                print("row {} in '{}' table does not have corresponding reference '{}' in '{}' table".format(
                    row,
                    self.referring_table_name,
                    self.key,
                    self.referred_table_name))
        else:
            print("No rows in '{}' table are missing a reference in table '{}' for '{}'".format(
                self.referring_table_name,
                self.referred_table_name,
                self.key))
        # print(self.__result__)

