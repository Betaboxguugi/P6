from test_predicates.t_predicate import TPredicate


class ReferentialPredicate(TPredicate):

    def __init__(self, conn):
        """
        :param conn: you know by now
        """
        self.warehouse = self.dictify(conn)
        self.referring_table = []
        self.referred_table = []
        """self.foreign_key_tables = {}
        self.foreign_keys = foreign_keys"""
        """for table_name, table in self.warehouse.items():
                if isinstance(foreign_key_tables, tuple)\
                        or isinstance(foreign_key_tables, list):
                    for foreign_key_table in foreign_key_tables:
                        if table_name == foreign_key_table:
                            self.foreign_key_tables[table_name] = table
                elif isinstance(foreign_key_tables, str):
                    if table_name == foreign_key_tables:
                        self.foreign_key_tables[table_name] = table
                else:  # TODO: exception if we end up here
                    pass"""

    def run(self, referring_table, referred_table, key):
        """
        :param referring_table:
        :param referred_table
        :param key
        """
        self.referring_table = self.warehouse.get(referring_table)
        self.referred_table = self.warehouse.get(referred_table)
        print(self.referring_table)
        print(self.referred_table)
        for referring_row in self.referring_table:
            flag = False
            print(referring_row)
            for referred_row in self.referred_table:
                print(referred_row)
                x = referring_row[key]
                y = referred_row[key]
                print(x)
                print(y)
                if x == y:
                    flag = True
                    print('match')
                    break
            if not flag:
                pass

        """# print(self.foreign_keys)
        # print(self.warehouse)
        keys = self.get_keys()
        foreign_keys = self.collect_foreign_key(keys)
        primary_keys = self.collect_primary_key(keys)"""
        """for foreign_key_table_name, foreign_key_table in self.foreign_key_tables.items():
            x = ()
            print(foreign_key_table_name)
            print(foreign_key_table)
            for table_name, table in self.warehouse.items():
                if table_name != foreign_key_table_name:
                    print(table_name)
                    for row in table:
                        print(row)"""

    def report(self):
        pass

