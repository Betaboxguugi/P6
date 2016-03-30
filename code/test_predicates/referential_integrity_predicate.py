from test_predicates.t_predicate import TPredicate



class ReferentialPredicate(TPredicate):

    def __init__(self, conn, foreign_key_tables):
        self.warehouse = self.dictify(conn)
        print(self.warehouse)
        for foreign_key_table in foreign_key_tables
        self.fact_table = self.warehouse.__getitem__(foreign_key_table)  # isolate the foreign_key_tables
        self.warehouse.__delitem__(foreign_key_table)                    # remove it from the other tables
        print(self.fact_table)                                    # how should this work for snowflake dimensions?
        print(self.warehouse)
        # TODO: make this work for a tuple of tables with foreign keys

    def run(self):
        pass

    def report(self):
        pass

