__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

from .predicate import Predicate
from ..predicate_report import Report


class ReferentialPredicate(Predicate):

    def __init__(self):
        self.missing_ft_keys = ()
        self.missing_dim_keys = ()
        self.referring_table_name = None
        self.referred_table_name = None
        self.dw_rep = None
        self.referring_table = None
        self.referred_table = None
        self.dw_dims = []
        self.dw_fts = []
        self.ft_dic = {}
        self.dim_dic = {}

    def run(self, dw_rep):
        self.dw_rep = dw_rep
        for dim in dw_rep.dims:
            self.dw_dims.append(dw_rep.get_data_representation(dim.name))
        for ft in dw_rep.fts:
            self.dw_fts.append(dw_rep.get_data_representation(ft.name))
        self.__result__ = True
        self.missing_ft_keys = ()
        self.missing_dim_keys = ()
        self.find_ft_refs()
        self.find_dim_refs()

        self.dim_check()  # TODO there is some funny business with overwriting the elements that fail the predicate
        self.ft_check()




    def find_ft_refs(self):
        """
        initiates the self.ft_dic to a dictionary of dictionaries like this:
        {'facttable1':{'bookid':'bookdim', 'timeid':'timedim', 'locationid':'locationdim'},
        'facttable2':{' ':' ', ' ':' ', ' ':' '}}
        With this we can lookup what facttables use what keys to reference which tables
        """
        for ft in self.dw_fts:
            keyref_dic = {}
            for keyref in ft.keyrefs:
                dims = self.dw_dims
                for dim in dims:
                    if keyref == dim.key:
                        keyref_dic[keyref] = dim.name
                        break
                self.ft_dic[ft.name] = keyref_dic

    def find_dim_refs(self):
        """
        See find_ft_refs above. initializes self.dim_dic to a dictionary of dictionaries like so:
        {'timedim': {'timeid': 'facttable'},
         'bookdim': {'bookid': 'facttable'},
         'locationdim': {'locationid': 'facttable'}}
        """
        for dim in self.dw_dims:
            keyref_dic = {}
            fts = self.dw_fts
            for ft in fts:
                for keyref in ft.keyrefs:
                    if keyref == dim.key:
                        keyref_dic[keyref] = ft.name
                        break
                self.dim_dic[dim.name] = keyref_dic

    def get_table(self, table_name):
        table = []
        for row in self.dw_rep.get_data_representation(table_name):
            table.append(row)
        return table

    def ft_check(self):
        for ft in self.dw_fts:
            flag = False
            fact_table = self.get_table(ft.name)
            for f_row in fact_table:
                key_dic = self.ft_dic.get(ft.name)
                for key, table_name in key_dic.items():
                    dim = self.dw_rep.tabledict.get(table_name)
                    for row in dim:
                        if row.get(key) == f_row.get(key):
                            flag = True
                            break
                    if not flag:
                        self.missing_ft_keys += ft.name, f_row,
                        self.__result__ = False

    def dim_check(self):
        for dim in self.dw_dims:
            flag = False
            dim_table = self.get_table(dim.name)
            for dim_row in dim_table:
                key_dic = self.dim_dic.get(dim.name)
                for key, table_name in key_dic.items():
                    ft = self.dw_rep.tabledict.get(table_name)
                    for row in ft:
                        if row.get(key) == dim_row.get(key):
                            flag = True
                            break
                    if not flag:
                        self.missing_dim_keys += dim.name, dim_row,
                        self.__result__ = False

    def report(self):
        if self.missing_ft_keys:
            if self.missing_dim_keys:
                missing_keys = self.missing_ft_keys, self.missing_dim_keys,
            else:
                missing_keys = self.missing_ft_keys
        elif self.missing_dim_keys:
            missing_keys = self.missing_dim_keys

        return Report(self.__class__.__name__,
                      self.__result__,
                      ': All is well',
                      ': All is not well',
                      missing_keys
                      )
"""
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
"""



