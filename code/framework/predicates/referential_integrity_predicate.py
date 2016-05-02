from .predicate import Predicate
from .predicate_report import Report
from framework.reinterpreter.datawarehouse_representation \
    import DimRepresentation, FTRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class ReferentialIntegrityPredicate(Predicate):

    def __init__(self):
        self.missing_ft_keys = []
        self.missing_dim_keys = []
        self.dw_rep = None
        self.dw_dims = []
        self.dw_fts = []
        self.ft_refs = {}
        self.dim_refs = {}

    def run(self, dw_rep):
        self.dw_rep = dw_rep
        for dim in dw_rep.dims:
            self.dw_dims.append(dw_rep.get_data_representation(dim.name))
        for ft in dw_rep.fts:
            self.dw_fts.append(dw_rep.get_data_representation(ft.name))

        self.__result__ = True
        self.missing_ft_keys = []
        self.missing_dim_keys = []
        self.ft_refs, self.dim_refs = self.find_refs()

        for dim, key_dic in self.dim_refs.items():
            for key in key_dic.keys():
                self.check_dim_to_table(dim, key)

        for ft, keyref_dic in self.ft_refs.items():
            for key in keyref_dic.keys():
                self.check_ft_to_table(ft, key)

        return self.report()

    def find_refs(self):
        ft_refs = {}
        dim_refs = {}
        refs = self.dw_rep.refs.copy()

        for table, tables in refs.items():
            if isinstance(table, DimRepresentation):
                dims = refs[table].copy()
                ref_dim = {}
                for attr in table.attributes:
                    for dim in dims:
                        if dim.key == attr:
                            dim_ref = {dim.key: table}
                            ref_dim[dim.key] = dim
                            dim_refs[dim] = dim_ref
                            dims.remove(dim)
                            break
                dim_refs[table] = ref_dim

            elif isinstance(table, FTRepresentation):
                dims = refs[table].copy()
                keyref_dic = {}
                for keyref in table.keyrefs:
                    for dim in dims:
                        if dim.key == keyref:
                            key_dic = {dim.key: table}
                            keyref_dic[keyref] = dim
                            dim_refs[dim] = key_dic
                            dims.remove(dim)
                            break
                ft_refs[table] = keyref_dic

        return ft_refs, dim_refs,

    def check_ft_to_table(self, ft, key):
        keyref_dic = self.ft_refs[ft]
        table = keyref_dic[key]
        for row in ft.itercolumns([key]):
            flag = False
            for table_row in table.itercolumns([key]):
                if row.get(key) == table_row.get(key):
                    flag = True
                    break
            if not flag:
                error_entry = "{} in {} not found in {}".format(row, ft.name,
                                                                table.name)
                if error_entry not in self.missing_ft_keys:
                    self.missing_ft_keys.append(error_entry)
                    self.__result__ = False

    def check_dim_to_table(self, dim, key):
        key_dic = self.dim_refs[dim]
        table = key_dic[key]
        for row in dim.itercolumns([key]):
            flag = False
            for table_row in table.itercolumns([key]):
                if row.get(key) == table_row.get(key):
                    flag = True
                    break
            if not flag:
                error_entry = "{} in {} not found in {}".format(row, dim.name,
                                                                table.name)
                if error_entry not in self.missing_dim_keys:
                    self.missing_dim_keys.append(error_entry)
                    self.__result__ = False

    def report(self):
        missing_keys = []
        if self.missing_ft_keys:
            if self.missing_dim_keys:
                for e in self.missing_ft_keys:
                    missing_keys.append(e)
                for e in self.missing_dim_keys:
                    missing_keys.append(e)
            else:
                for e in self.missing_ft_keys:
                    missing_keys.append(e)
        elif self.missing_dim_keys:
            for e in self.missing_dim_keys:
                    missing_keys.append(e)

        report = Report(self.__result__, self.__class__.__name__, missing_keys,
                        'Something went wrong. {} returned false without '
                        'failed entries. This should never happen.'.format(
                          self.__class__.__name__)
                        )
        return report
