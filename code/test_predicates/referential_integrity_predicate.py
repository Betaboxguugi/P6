from test_predicates.t_predicate import TPredicate


class ReferentialPredicate(TPredicate):

    def __init__(self, conn, foreign_key_tables, foreign_keys):
        """
        :param foreign_keys:
        :param conn: you know by now
        :param foreign_key_tables: a string of one table name or tuple of table names that need their foreign keys
        tested
        """
        self.warehouse = self.dictify(conn)
        self.foreign_key_tables = {}
        self.foreign_keys = foreign_keys
        for table_name, table in self.warehouse.items():
                if isinstance(foreign_key_tables, tuple)\
                        or isinstance(foreign_key_tables, list):
                    for foreign_key_table in foreign_key_tables:
                        if table_name == foreign_key_table:
                            self.foreign_key_tables[table_name] = table
                elif isinstance(foreign_key_tables, str):
                    if table_name == foreign_key_tables:
                        self.foreign_key_tables[table_name] = table
                else:  # TODO: exception if we end up here
                    pass

    def run(self):
        """

        """
        for foreign_key_table_name, foreign_key_table in self.foreign_key_tables.items():
            print(foreign_key_table_name)
            print(foreign_key_table)
            for table_name, table in self.warehouse.items():
                if table_name != foreign_key_table_name:
                    print(table_name)
                    for row in table:
                        print(row)
                        flag = False
                        for key in self.foreign_keys:
                            x = row.get(key)
                            if x:
                                print(x)
                                flag = True
                                break

    def report(self):
        pass

