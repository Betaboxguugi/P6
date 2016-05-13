from .predicate import Predicate
from .report import Report
from framework.reinterpreter.datawarehouse_representation \
    import FTRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class ReferentialIntegrityPredicate(Predicate):
    def __init__(self, refs={}):
        self.dw_rep = None
        self.refs = refs
        self.missing_keys = []

    def run(self, dw_rep):



        self.missing_keys = []


        if not self.refs:
            self.refs = dw_rep.refs


        for table,dims in self.refs.items():
            for dim in dims:
                key = dw_rep.get_representation(dim).key

                table_to_dim_sql =\
                    " SELECT * " + \
                    " FROM " + table + \
                    " WHERE " + key + " NOT EXISTS( SELECT* FROM " + dim + " )"







        SELECT *
        FROM alpha
        WHERE key NOT IN(alpha NATURAL JOIN beta)
        UNION
        SELECT *
        FROM beta
        WHERE key NOT IN(alpha NATURAL JOIN beta)


        self.refs = self._find_refs()
        for table, key_dic in self.refs.items():
            for key in key_dic.keys():
                self._check_ref(table, key)

        tables = []
        for key in self.refs.keys():
            tables.append(key.name)
        return Report(self.__result__, self,
                      tables,
                      self.missing_keys,
                      )
