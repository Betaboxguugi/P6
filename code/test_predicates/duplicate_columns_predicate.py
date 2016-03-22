from code.test_predicates.t_predicate import TPredicate


class DuplicatePredicate(TPredicate):


    def __init__(self, conn):
        """"""
        self.__result__ = False
        self.table = self.dictify(conn)
        self.table_name = ''
        self.columns = ()


    def run(self, table_name, columns):
        self.table_name = table_name
        print(self.table[self.table_name])
        abc = self.table[self.table_name].pop(0)
        print(abc)
        print(abc.get('AGE'))
