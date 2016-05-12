__author__ = 'Alexander Brandborg'
__maintainer__='Alexander Brandborg'

from .predicate import Predicate
from ..reinterpreter.datawarehouse_representation import \
    SCDType2DimRepresentation
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
        self.table = table_name
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

        dim = dw_rep.get_data_representation(self.table)

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
        null_condition_sql = \
            (x + " IS NULL" for x in self.entry)

        lookup_sql = " SELECT " + versionatt + \
                     " NATURAL JOIN ".join(self.table_name) + \



        WITH matchingrow AS(
SELECT versionatt
FROM <join>
WHERE A = lookupatt.A (osv.)
)

SELECT max(*)
FROM matchingRow


        largest_version = None
        for row in dim.itercolumns(columns_to_get):

            # Gets only the lookupatts subset of the row
            row_lookupatts = {key: value for key, value in row.items() if
                      key in lookupatts}

            # If the row corresponds to the test entry
            if row_lookupatts == self.entry:
                row_version = row[versionatt]
                if largest_version is None or largest_version < row_version:
                    largest_version = row_version

        return Report(result=largest_version == self.version,
                      tables=self.table,
                      predicate=self,
                      elements=(),
                      msg='Version number not as asserted. ' +
                          'Was asserted to be ' + str(self.version) +
                          ',but was instead ' + str(largest_version))

