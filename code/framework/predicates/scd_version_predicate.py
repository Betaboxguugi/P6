__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'

from framework.datawarehouse_representation import \
    SCDType2DimRepresentation
from .predicate import Predicate
from .report import Report


class SCDVersionPredicate(Predicate):
    """
     Predicate that can check whether a specific entry in a Type2SCD has an
     asserted maximum version.
    """

    def __init__(self, table_name, entry, version):
        """
        :param table_name: Name of Type2SCD table
        :param entry: Row giving lookupsatts with values
        :param version: The asserted maximum version of the entry.
        :return:
        """
        self.table_name = table_name
        self.entry = entry
        self.version = version

    def run(self, dw_rep):
        """
        For each entry in the table, it checks whether it corresponds,
        to the test entry. If it does we check whether we need to update
        the currently largest discovered version for that entry.
        :param dw_rep: A DWRepresentation object
        :return report object describing results of the predicate
        """

        dim = dw_rep.get_data_representation(self.table_name)

        if not isinstance(dim, SCDType2DimRepresentation):
            raise RuntimeError('Given table is not'
                               ' a SCDType2DimRepresentation')

        if not set(dim.lookupatts) == set(self.entry.keys()):
            raise RuntimeError('Correct lookupatts not given')

        lookupatts = dim.lookupatts
        versionatt = dim.versionatt

        columns_to_get = list(lookupatts)
        columns_to_get.append(versionatt)

        self.entry.keys()

        null_condition_sql = []
        for a,b in self.entry.items():
            if isinstance(b,str):
                new = "\'" + b + "\'"
                null_condition_sql.append(a + " = " + new)

            else:
                null_condition_sql.append(a + " = " + str(b))

        lookup_sql = " SELECT max(" + versionatt + ")" \
                     " FROM " + self.table_name + \
                     " WHERE " + " AND ".join(null_condition_sql)

        cursor = dw_rep.connection.cursor()
        cursor.execute(lookup_sql)
        (query_result,) = cursor.fetchall()

        if query_result[0] is None:
            raise RuntimeError('Table empty or Row not found')

        if query_result[0] == self.version:
            self.__result__ = True

        return Report(result=self.__result__,
                      tables=self.table_name,
                      predicate=self,
                      elements=(),
                      msg='Version number not as asserted. ' +
                          'Was asserted to be ' + str(self.version) +
                          ',but was instead ' + str(query_result[0]))

