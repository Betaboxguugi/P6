from .predicate import Predicate
from .report import Report
from framework.reinterpreter.datawarehouse_representation \
    import FTRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class ReferentialIntegrityPredicate(Predicate):
    def __init__(self):
        self.dw_rep = None
        self.refs = {}
        self.missing_keys = []

    def run(self, dw_rep):
        self.dw_rep = dw_rep
        self.missing_keys = []
        self.__result__ = True
        self.refs = self._find_refs()
        for table, key_dic in self.refs.items():
            for key in key_dic.keys():
                self._check_ref(table, key)

        return self.report()

    def _find_refs(self):
        """
        This method is used to gather information using the refs dictionary in
        the dw_rep. The dictionary shows what tables a table has references to,
        but it holds no information about which foreign key is used to do this.
        That is the information this method retrieves.
        :return a Dictionary of dictionaries, with table reps as key for the
        outer dict, and foreign keys for the inner dictionaries which contain
        the table reps that are referenced
        """
        result_refs = {}
        for table, dims in self.dw_rep.refs.items():
            if isinstance(table, FTRepresentation):
                attributes = table.keyrefs
            else:
                attributes = table.attributes
            ref_dim = {}
            for attr in attributes:
                for dim in dims:
                    # We attempt to find a common attribute/key between the
                    # tables. Between a facttable and dimension or dimensions
                    # in snowflaking, there should always be an
                    # attribute or keyref with the same name as the dimension
                    # key
                    if dim.key == attr:
                        ref_dim[dim.key] = dim
                        break
            result_refs[table] = ref_dim

        return result_refs

    def _check_ref(self, table, key):
        """
        :param table: Table to have its referential integrity checked on a
        foreign key
        :param key: foreign key used to check referential integrity
        """
        keyref_dic = self.refs[table]
        dim = keyref_dic[key]
        for row in table.itercolumns([key]):
            flag = False
            for dim_row in dim.itercolumns([key]):
                if row.get(key) == dim_row.get(key):
                    flag = True
                    break
            if not flag:
                error_entry = "{} in {} not found in {}".format(row,
                                                                table.name,
                                                                dim.name)
                if error_entry not in self.missing_keys:
                    self.missing_keys.append(error_entry)
                    self.__result__ = False

        # We check for referential integrity backwards as the dictionary
        # does not hold information about this
        for row in dim.itercolumns([key]):
            flag = False
            for table_row in table.itercolumns([key]):
                if row.get(key) == table_row.get(key):
                    flag = True
                    break
            if not flag:
                error_entry = "{} in {} not found in {}".format(row,
                                                                dim.name,
                                                                table.name)
                if error_entry not in self.missing_keys:
                    self.missing_keys.append(error_entry)
                    self.__result__ = False

    def report(self):
        tables = []
        for key in self.refs.keys():
            tables.append(key.name)
        report = Report(self.__result__, self,
                        tables,
                        self.missing_keys,
                        )
        return report
