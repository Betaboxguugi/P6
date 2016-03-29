from code.test_predicates.t_predicate import TPredicate


class DuplicatePredicate(TPredicate):


    def __init__(self, conn):
        """"""
        self.table = self.dictify(conn)
        self.table_name = ''
        self.columns = ()
        self.__result__ = []


    def run(self, table_name, columns):
        self.table_name = table_name
        self.table = self.table[self.table_name]
        self.columns = columns
        self.remove_unique()

    def remove_unique(self):
        self.columns = sorted(self.columns)
        while len(self.table) > 1:
            dic = self.table.pop(0)
            for row in self.table:
                print("Looking at table {}".format(self.table))
                print("Checking table against row: {}".format(dic))
                print("Checking table row: {}".format(row))
                flag = False
                for x in self.columns:
                    element = dic.get(x)
                    print("Looking at column {}".format(x))
                    print("Looking for {} with key {}".format(element, x))
                    y = row.get(x)
                    print("Found value {}".format(y))
                    if element != y:
                        print('Unique')
                        flag = False
                        break
                    else:
                        print('Duplicate value')
                        flag = True
                if flag:
                    print('Duplicate row found')
                    self.__result__.append(dic)
        print(self.__result__)
